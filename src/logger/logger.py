from logger.logger_levels import LoggerLevels
from logger.logger_levels import from_logger_level

from time import time

class Logger:
    def __init__(self, debug: bool, log: bool):
        self.is_debug = debug
        self.is_logging = log

    def info(self, message: str):
        if not self.is_logging:
            return
        
        data = self._format_message(LoggerLevels.INFO, message)
        print(data)

    def warning(self, message: str):
        if not self.is_logging:
            return
        
        data = self._format_message(LoggerLevels.WARNING, message)
        print(data)

    def error(self, message: str):
        if not self.is_logging:
            return
        
        data = self._format_message(LoggerLevels.ERROR, message)
        print(data)

    def debug(self, message: str):
        if not self.is_logging:
            return
        
        if self.is_debug:
            data = self._format_message(LoggerLevels.DEBUG, message)
            print(data)

    @staticmethod
    def _format_message(level: LoggerLevels, message: str):
        return f'{time()} {level} {from_logger_level(level)} {message}'
