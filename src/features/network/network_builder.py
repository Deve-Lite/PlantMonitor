from ujson import loads

from features.logger.logger import Logger
from features.logger.logger_levels import LoggerLevels
from features.network.connection import ConnectionConfiguration, ConnectionTypes, Connection
from features.network.wifi import WiFi


class NetworkBuilder:
    def __init__(self, logger: Logger=None):
        self.config = loads("configuration/connection.py")
        if logger is None:
            self.logger = Logger(LoggerLevels.DEBUG)
        else:
            self.logger = logger

    def build(self):
        config = ConnectionConfiguration(self.config)

        if config.type == ConnectionTypes.WiFi:
            return WiFi(self.logger, config)

        return Connection(self.logger, config)
