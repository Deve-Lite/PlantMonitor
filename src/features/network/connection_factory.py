from abstractions.factory import Factory
from features.logger.logger import Logger
from features.network.connection import ConnectionConfiguration, ConnectionTypes, Connection
from features.network.wifi import WiFi


class ConnectionFactory(Factory):
    def __init__(self, logger: Logger = None):
        super().__init__("connection", logger)

    def create(self):
        config = ConnectionConfiguration(self.config)

        if config.type == ConnectionTypes.WiFi:
            return WiFi(self.logger, config)

        return Connection(self.logger, config)
