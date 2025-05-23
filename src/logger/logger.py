from features.logger.logger_levels import LoggerLevels
from features.logger.logger_levels import from_logger_level

from utime import time

class Logger:
    def __init__(self, debug: bool):
        self.is_debug = debug

    def info(self, message: str):
        data = self._format_message(LoggerLevels.INFO, message)
        print(data)

    def warning(self, message: str):
        data = self._format_message(LoggerLevels.WARNING, message)
        print(data)

    def error(self, message: str):
        data = self._format_message(LoggerLevels.ERROR, message)
        print(data)

    def debug(self, message: str):
        if self.is_debug:
            data = self._format_message(LoggerLevels.DEBUG, message)
            print(data)

    @staticmethod
    def _format_message(level: LoggerLevels, message: str):
        return f'{time()} {level} {from_logger_level(level)} {message}'
