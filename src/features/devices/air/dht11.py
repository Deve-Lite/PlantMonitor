from features.devices.device import Device, DeviceConfig, Topic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff
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
        super().__init__(mqtt, config)
        self.logger = logger
        self.unit_topic = config["unitTopic"]

    def update_unit(self, payload: str):
        collection = loads(payload)
        new_unit = collection["unit"]

        if new_unit not in self.AVAILABLE_UNITS:
            self.logger.log_warning(f"Unit {new_unit} is not supported. Supported units: {self.AVAILABLE_UNITS}")
            return

        self.unit = new_unit
        self.logger.log_info(f"Unit changed to {new_unit}")

    def format_data(self):
        value = self._convert_unit(self.value)

        if not self.sendAsJson:
            return value

        json = {
            "unit": self.unit,
            "value": value,
            "time": self._last_update
        }

        return dumps(json)

    def _convert_unit(self, value):
        if self.unit == "F" or "Fahrenheit":
            return self.celsius_to_fahrenheit(value)

        if self.unit == "K" or "Kelvin":
            return self.celsius_to_kelvin(value)

        return value

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return fahrenheit

    @staticmethod
    def celsius_to_kelvin(celsius):
        kelvin = celsius + 273.15
        return kelvin


class DHT11(Device):
    DHT_READ_SPAN = 2000

    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger):
        super().__init__(mqtt, config, logger)
        data = config.config["data"]

        self.data_pin = data["pin"]
        self._temperature = Temperature(mqtt, data["temperature"], logger)
        self._humidity = Humidity(mqtt, data["humidity"])

        dht_pin = machine.Pin(self.data_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._sensor = dht.DHT11(dht_pin)

        self._last_read = ticks_ms()

        unit_topic = f"{self.base_topic}/{self._temperature.unit_topic}"
        self.mqtt.subscribe(unit_topic, self._temperature.update_unit)

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()
        if abs(ticks_diff(current_time, self._last_read)) < DHT11.DHT_READ_SPAN:
            uasyncio.sleep_ms(200)
            return

        self.logger.log_info(f"Starting loop of dht11 sensor ar {current_time}.")
        self._last_read = current_time
        self._sensor.measure()

        self._temperature.update(self.base_topic, current_time, self._sensor.temperature())
        self._humidity.update(self.base_topic, current_time, self._sensor.humidity())

        self.logger.log_debug(f"Temperature: {self._sensor.temperature()}, humidity: {self._sensor.humidity()}.")
