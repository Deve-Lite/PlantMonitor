from features.logger.logger import Logger
from ujson import loads

from features.logger.logger_levels import LoggerLevels


class Factory:
    def __init__(self, config_name, logger: Logger = None):
        if logger is None:
            self.logger = Logger(LoggerLevels.DEBUG)
        else:
            self.logger = logger

        path = f"configuration/{config_name}.json"
        logger.log_info(f"Reading configuration from: {path}")
        with open(path, 'r') as file:
            json_file = file.read()
        self.config = loads(json_file)
    
    def create(self):
        raise NotImplementedError("Method not implemented")
