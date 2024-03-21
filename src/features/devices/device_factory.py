from abstractions.factory import MultiFactory
from features.logger.logger import Logger
from features.devices.air.dht11 import DHT11
from features.devices.device import DeviceConfig


class DeviceFactory(MultiFactory):
    def __init__(self, client, logger: Logger):
        super().__init__("devices", logger)
        self.logger = logger
        self.client = client
        self.max_items = 48

    def _create(self, config):
        config = DeviceConfig(config)

        if config.type == "air":
            if config.name == "dht11":
                return DHT11(self.client, config, self.logger)
            raise NotImplementedError("Air device is not supported")

        raise NotImplementedError(f"Device {config.type}-{config.name} is not supported")
