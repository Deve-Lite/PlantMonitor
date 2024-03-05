from abstractions.builder import Builder
from features.logger.logger import Logger
from features.network.connection import ConnectionConfiguration, ConnectionTypes, Connection
from features.network.wifi import WiFi


class ConnectionBuilder(Builder):
    def __init__(self, logger: Logger = None):
        super().__init__("connection", logger)

    def build(self):
        config = ConnectionConfiguration(self.config)

        if config.type == ConnectionTypes.WiFi:
            return WiFi(self.logger, config)

        return Connection(self.logger, config)
