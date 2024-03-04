from features.logger.logger import Logger


class App:
    def __init__(self, logger: Logger):
        self._logger = logger

    def start(self):
        self._logger.log_debug("Starting device loop.")
