from features.logger.logger import Logger
from ujson import loads

from features.logger.logger_levels import LoggerLevels


class Builder:
    def __init__(self, config_name, logger: Logger=None):
        if logger is None:
            self.logger = Logger(LoggerLevels.DEBUG)
        else:
            self.logger = logger
        self.config = loads(f"configuration/{config_name}.json")