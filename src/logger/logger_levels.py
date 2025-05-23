class LoggerLevels:
    INFO = 0
    WARNING = 1
    ERROR = 2
    DEBUG = -1


def to_logger_level(level: str):
    if level == "info":
        return LoggerLevels.INFO
    if level == "warning":
        return LoggerLevels.WARNING
    if level == "error":
        return LoggerLevels.ERROR

    return LoggerLevels.DEBUG


def from_logger_level(level: LoggerLevels):
    if level == LoggerLevels.INFO:
        return "info"
    if level == LoggerLevels.WARNING:
        return "warning"
    if level == LoggerLevels.ERROR:
        return "error"

    return "debug"
