from abstractions.factory import Factory
from features.logger.logger import Logger
from features.UI.LCD.lcd import MyLCDConfig
from features.UI.LCD.lcd import MyLCD

class MyLCDFactory(Factory):
    def __init__(self, logger: Logger = None):
        super().__init__("ui", logger)

    def create(self):
        config = MyLCDConfig(self.config)

        return MyLCD(config)