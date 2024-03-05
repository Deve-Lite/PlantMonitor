from abstractions.builder import Builder
from features.logger.logger import Logger
from features.mqtt.hive_mq import HiveMqClient
from features.mqtt.mqtt import MqttConfiguration, MqttTypes, BaseMqttClient


class MqttBuilder(Builder):
    def __init__(self, logger: Logger = None):
        super().__init__("mqtt", logger)

    def build(self):
        config = MqttConfiguration(self.config)

        if config.type == MqttTypes.HiveMq:
            return HiveMqClient(config, self.logger)

        return BaseMqttClient(config, self.logger)