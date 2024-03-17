from abstractions.factory import Factory
from features.logger.logger import Logger
from features.mqtt.hive_mq import HiveMqClient
from features.mqtt.mqtt import MqttConfiguration, MqttTypes, BaseMqttClient


class MqttFactory(Factory):
    def __init__(self, logger: Logger = None):
        super().__init__("mqtt", logger)

    def create(self):
        config = MqttConfiguration(self.config)

        if config.type == MqttTypes.HiveMq:
            return HiveMqClient(config, self.logger)

        return BaseMqttClient(config, self.logger)