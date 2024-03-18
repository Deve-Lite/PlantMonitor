from abstractions.factory import Factory
from features.logger.logger import Logger
from features.devices.air.dht11 import DHT11
from features.devices.device import DeviceConfig


class DeviceFactory(Factory):
    def __init__(self, client, logger: Logger):
        self.logger = logger
        self.client = client

    def create(self, config: DeviceConfig):

        if config.type == "TemperatureAndHumidity":
            if config.name == "dht11":
                return DHT11(self.client, config, self.logger)
            raise NotImplementedError("Air device is not supported")

        raise NotImplementedError("Device is not supported")
