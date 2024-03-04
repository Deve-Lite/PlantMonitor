from application import App
from features.logger.logger import Logger
from features.logger.logger_levels import LoggerLevels

from utime import sleep

import gc

logger = Logger(LoggerLevels.DEBUG)

if __name__ == '__main__':
    gc.collect()
    try:
        pass
    except Exception as e:
        logger.log_info(f"Exception occurred when device was initializing")


    app = App(logger)

    app.start()