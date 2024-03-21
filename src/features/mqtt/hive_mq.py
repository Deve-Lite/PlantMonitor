from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient, MqttConfiguration
from umqtt.robust import MQTTClient


class HiveMqClient(BaseMqttClient):
    def __init__(self, mqtt_config: MqttConfiguration, logger: Logger):
        super().__init__(mqtt_config, logger)
        self._base_topic = mqtt_config.json.get("typeSpecificData", {}).get("baseTopic", "")

        authentication_data = self.config.json.get("authentication")
        username = authentication_data.get("data", {}).get("username", "")
        password = authentication_data.get("data", {}).get("password", "")
        self.logger.log_debug(f"Connecting to server with: {username} {password}")
        self._client = MQTTClient(
            client_id=self.config.client,
            server=self.config.server,
            port=self.config.port,
            user=username,
            password=password,
            keepalive=self.config.keep_alive,
            ssl=True,
            ssl_params={"server_hostname": self.config.server})

        self._client.set_callback(self.callback)

    def format_topic(self, topic):
        if self._base_topic is "":
            return super().format_topic(topic)

        topic = f"{self._base_topic}{topic}"
        self.logger.log_debug(f"Topic formatted: {topic}")
        return topic

    def callback(self, topic, message):
        try:
            topic = topic.decode("utf-8")
            data = message.decode("utf-8")

            self.logger.log_info(f"Data from topic '{topic}' received. ")
            self.logger.log_debug(f"Received Topic: '{topic}' Payload: {data}. ")

            if topic not in self.callbacks:
                self.logger.log_warning(f"{topic} not found in topics. Ignoring message")
                return

            function = self.callbacks[topic]
            function(data)

        except Exception as e:
            self.logger.log_error(f"Error receiving data on {topic}. Error {e}")

    def update(self):
        self.logger.log_info(f"Fetching data from broker: {self.config.server}")
        self._client.check_msg()

    def connect(self):
        try:
            self.logger.log_info(f"Connecting to broker: {self.config.server}")
            self._client.connect()
            self.logger.log_info(f"Successfully connected to broker: {self.config.server}")
            return True
        except Exception as e:
            self.logger.log_info(f"Failed to connect to broker: {self.config.server}")
            self.logger.log_info(f"Connection error {e}")
            return False

    def publish(self, topic: str, payload: str):
        topic = self.format_topic(topic)
        topic_bytes = topic.encode('utf-8')
        payload_bytes = payload.encode('utf-8')

        self._values[topic] = payload
        self._client.publish(topic_bytes, payload_bytes)
        self.logger.log_info(f"Published data on topic {topic}")
        self.logger.log_debug(f"Sending Topic: '{topic}' Payload: {payload}. ")

    def subscribe(self, topic: str, callback):
        topic = self.format_topic(topic)
        self._client.subscribe(topic)
        self.callbacks[topic] = callback
        self.logger.log_info(f"Subscribed to topic: {topic}")

