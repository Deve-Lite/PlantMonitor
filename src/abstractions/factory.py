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
        logger.info(f"Reading configuration from: {path}")
        with open(path, 'r') as file:
            json_file = file.read()
        self.config = loads(json_file)
    
    def create(self):
        raise NotImplementedError("Method not implemented")


class MultiFactory(Factory):
    def __init__(self, config_name, logger: Logger = None):
        super().__init__(config_name, logger)
        self.max_items = 1

    def _create_item(self, config):
        raise NotImplementedError("Method not implemented")

    def create(self):
        if len(self.config) == 0:
            return []

        if len(self.config) >= self.max_items:
            raise ValueError(f"Number of items exceeds the maximum number of items: {self.max_items} actual {len(self.config)}")

        items = []

        for item_config in self.config:
            item = self._create_item(item_config)
            items.append(item)

        return items
