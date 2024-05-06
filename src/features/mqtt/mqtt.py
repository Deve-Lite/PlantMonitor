from abstractions.configuration import Configuration
from features.logger.logger import Logger

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
        self.port = self.value_in_range(name="port", min_v=0, max_v=65536)
        self.client = json.get("client")
        self.ssl = json.get("ssl", True)
        self.keep_alive = self.value_in_range(name="keepAlive", min_v=10, max_v=120)


class BaseMqttClient:
    def __init__(self, mqtt_config: MqttConfiguration, logger: Logger):
        self.config = mqtt_config
        self.logger = logger
        self.callbacks = {}
        self._values = {}

    def get_values(self, topic_base: str):
        return {k: v for k, v in self._values.items() if k.startswith(topic_base)}

    def format_topic(self, topic: str):
        self.logger.debug(f"Topic not formatted: {topic}")
        return topic

    def update(self):
        self.logger.info("Fake fetching data from broker.")
        pass

    def connect(self):
        self.logger.info(f"Fake connect to MQTT Broker.")
        return True

    def publish(self, topic: str, json_data: str):
        self.logger.info(f"Fake publish on topic: {topic} data: {json_data}")

    def subscribe(self, topic: str, callback):
        topic = self.format_topic(topic)
        self.logger.info(f"Subscribed to topic: {topic}")
        self.callbacks[topic] = callback

