from features.logger.logger_levels import LoggerLevels
from features.logger.logger_levels import from_logger_level


class Logger:
    def __init__(self, level: LoggerLevels):
        self.level = level

    def log_info(self, message: str):
        data = self._format_message(LoggerLevels.INFO, message)
        print(data)

    def log_warning(self, message: str):
        data = self._format_message(LoggerLevels.WARNING, message)
        print(data)

    def log_error(self, message: str):
        data = self._format_message(LoggerLevels.ERROR, message)
        print(data)

    def log_debug(self, message: str):
        if self.level == LoggerLevels.DEBUG:
            data = self._format_message(LoggerLevels.DEBUG, message)
            print(data)

    @staticmethod
    def _format_message(level: LoggerLevels, message: str):
        return f'{level} {from_logger_level(level)} {message}'
