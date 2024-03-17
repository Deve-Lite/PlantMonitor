from abstractions.factory import Factory
from features.logger.logger import Logger
from features.devices.air.dht11 import DHT11


class DeviceFactory(Factory):
    def __init__(self, mqtt_client, logger: Logger):
        self.logger = logger
        self.mqtt_client = mqtt_client

    def create(self, device_config):

        if device_config.type == "TemperatureAndHumidity":
            if device_config.name == "dht11":
                return NotImplementedError("DHT11 is not supported")
            raise NotImplementedError("Air device is not supported")

        raise NotImplementedError("Device is not supported")
