from features.devices.device import Device, DeviceConfig, Topic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff, time
from ujson import dumps, loads
import machine
import dht
import uasyncio


class Humidity(Topic):
    pass


class Temperature(Topic):
    AVAILABLE_UNITS = ["C", "F", "K",
                       "Celsius", "Fahrenheit", "Kelvin"]

    def __init__(self, mqtt: BaseMqttClient, config, logger: Logger):
        super().__init__(mqtt, config, logger)
        self.unit_topic = config["unitTopic"]

    def update_unit(self, payload: str):
        collection = loads(payload)
        new_unit = collection["unit"]

        if new_unit not in self.AVAILABLE_UNITS:
            self.logger.warning(f"Unit {new_unit} is not supported. Supported units: {self.AVAILABLE_UNITS}")
            return

        self.unit = new_unit
        self.logger.info(f"Unit changed to {new_unit}")

    def format_data(self):
        value = self._convert_unit(self._value)

        if not self.sendAsJson:
            return value

        json = {
            "value": value,
            "unit": self.unit,
            "time": time(),
            "timeUnit": "s"
        }

        return dumps(json)

    def _convert_unit(self, value):
        if self.unit in ["F", "Fahrenheit"]:
            return self.celsius_to_fahrenheit(value)

        if self.unit in ["K", "Kelvin"]:
            return self.celsius_to_kelvin(value)

        return value

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return int(fahrenheit)

    @staticmethod
    def celsius_to_kelvin(celsius):
        kelvin = celsius + 273.15
        return int(kelvin)


class DHT11(Device):
    DHT_READ_SPAN = 2000

    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger):
        super().__init__(mqtt, config, logger)
        data = config.config

        self.data_pin = data["pin"]
        self._temperature = Temperature(mqtt, data["temperature"], logger)
        self._humidity = Humidity(mqtt, data["humidity"], logger)
        self.loop_span_ms = data["loopSpanMs"]

        dht_pin = machine.Pin(self.data_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._sensor = dht.DHT11(dht_pin)

        self._last_read = ticks_ms() - self.DHT_READ_SPAN

        unit_topic = f"{self.base_topic}/{self._temperature.topic}/{self._temperature.unit_topic}"
        self.mqtt.subscribe(unit_topic, self._temperature.update_unit)

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()

        if abs(ticks_diff(current_time, self._last_read)) < DHT11.DHT_READ_SPAN:
            await uasyncio.sleep_ms(self.loop_span_ms)
            return

        self._last_read = current_time
        self._sensor.measure()

        self._temperature.update(self.base_topic, current_time, self._sensor.temperature())
        self._humidity.update(self.base_topic, current_time, self._sensor.humidity())

        self.logger.debug(f"Temperature: {self._sensor.temperature()}")
        self.logger.debug(f"Humidity: {self._sensor.humidity()}.")

        await uasyncio.sleep_ms(self.loop_span_ms)


