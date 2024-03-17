from features.devices.device import Device, DeviceConfig, Topic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff
from ujson import dumps
import machine
import dht
import uasyncio


class Humidity(Topic):
    pass


class Temperature(Topic):
    pass

    #TODO: Implement temperature conversion
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return fahrenheit

    @staticmethod
    def celsius_to_kelvin(celsius):
        kelvin = celsius + 273.15
        return kelvin


class DHT11Config:
    def __init__(self, mqtt: BaseMqttClient, config: {}):
        device_data = config["data"]
        self.data_pin = device_data["pin"]
        self.temperature = Temperature(mqtt, device_data["temperature"])
        self.humidity = Humidity(mqtt, device_data["humidity"])


class DHT11(Device):
    DHT_READ_SPAN = 2000

    def __init__(self, mqtt_client: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger):
        super().__init__(mqtt_client, config, logger)
        self._device_config = DHT11Config(config.config)
        dht_pin = machine.Pin(self._device_config.data_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._sensor = dht.DHT11(dht_pin)
        self._humidity = None
        self._temp = None
        self._last_read = ticks_ms()

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

        base_topic = self.topic()
        # TODO: Implement values updates
        temp = self._sensor.temperature()
        humidity = self._sensor.humidity()

        self.logger.log_debug(f"Measured temperature: {temp} and humidity: {humidity}.")
