from abstractions.configuration import Configuration
from features.logger.logger import Logger


class ConnectionConfiguration(Configuration):
    def __init__(self, json):
        super().__init__(json)
        self.type = self.value_in_list("type", ConnectionTypes.get_types())
        self.ssid = json.get("ssid")
        self.password = json.get("password")
        self.max_connection_tries = self.value_in_range(name="maxConnectionTime", min_v=5, max_v=60)


class ConnectionTypes:
    Fake = "none"
    WiFi = "wifi"

    @classmethod
    def get_types(cls):
        return [ConnectionTypes.Fake, ConnectionTypes.WiFi]


class Connection:
    def __init__(self, logger: Logger, config: ConnectionConfiguration):
        self.config = config
        self.logger = logger

    def is_connected(self):
        self.logger.log_debug("Fake. Connected to wifi.")
        return True

    def connect(self):
        self.logger.log_debug("Fake. Connecting to wifi...")
        return True
