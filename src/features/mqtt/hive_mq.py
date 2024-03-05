from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient, MqttConfiguration
from umqtt.simple import MQTTClient

class HiveMqClient(BaseMqttClient):
    def __init__(self, mqtt_config: MqttConfiguration, logger: Logger):
        super().__init__(mqtt_config, logger)
        self._base_topic = mqtt_config.json.get("typeSpecificData", {}).get("baseTopic", "")
        self._subscribed = []

        authentication_data = mqtt_config.json.get("authentication")

        username = authentication_data.json.get("data", {}).get("username", "")
        password = authentication_data.json.get("data", {}).get("password", "")


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

    def callback(self, topic, message):
        pass