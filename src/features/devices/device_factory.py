from abstractions.factory import MultiFactory
from features.analog_accessor.analog_accessor import AnalogAccessor
from features.logger.logger import Logger
from features.devices.air.dht11 import DHT11
from features.devices.device import DeviceConfig
from features.mqtt.mqtt import BaseMqttClient


class DeviceFactory(MultiFactory):
    def __init__(self, client: BaseMqttClient, analog_accessors: [AnalogAccessor], logger: Logger):
        super().__init__("devices", logger)
        self.logger = logger
        self.client = client
        self.analog_accessors = analog_accessors
        self.max_items = 48

    def _create_item(self, config):
        config = DeviceConfig(config)

        if config.type == "air":
            if config.name == "dht11":
                return DHT11(self.client, config, self.logger)
            raise NotImplementedError("Air device is not supported")

        raise NotImplementedError(f"Device {config.type}-{config.name} is not supported")
