from abstractions.factory import Factory
from logger.logger import Logger
from UI.Encoder.encoder import EncoderConfig
from UI.Encoder.encoder import RotaryEncoder

class EncoderFactory(Factory):
    def __init__(self, logger: Logger = None):
        super().__init__("ui", logger)

    def create(self):
        config = EncoderConfig(self.config)

        return RotaryEncoder(config)