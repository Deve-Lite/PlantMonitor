from abstractions.configuration import Configuration
from features.logger.logger import Logger

from ujson import loads

class MqttTypes:
    Fake = "none"
    HiveMq = "hivemq"

    @classmethod
    def get_types(cls):
        return [MqttTypes.Fake, MqttTypes.HiveMq]


class MqttConfiguration(Configuration):
    def __init__(self, json: {}):
        super().__init__(json)
        self.type = self.value_in_list("type", MqttTypes.get_types())
        self.server = json.get("server")
        self.port = self.value_in_range("port", 0, 65536)
        self.client = json.get("client")
        self.ssl = json.get("sll", True)
        self.keep_alive = self.value_in_range("keep_alive", 10, 60)


class BaseMqttClient:
    def __init__(self, mqtt_config: MqttConfiguration, logger: Logger):
        self.config = mqtt_config
        self.logger = logger
        self.callbacks = {}

    def format_topic(self, topic):
        self.logger.log_debug(f"Topic not formatted: {topic}")
        return topic

    def update(self):
        self.logger.log_info("Fake fetching data from broker.")
        pass

    def connect(self):
        self.logger.log_info(f"Fake connect to MQTT Broker.")
        return True

    def publish(self, topic: str, json_data: str):
        self.logger.log_info(f"Fake publish on topic: {topic} data: {json_data}")

    def subscribe(self, topic: str, callback):
        topic = self.format_topic(topic)
        self.logger.log_info(f"Subscribed to topic: {topic}")
        self.callbacks[topic] = callback