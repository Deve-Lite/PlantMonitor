from abstractions.factory import Factory

from features.UI.Encoder.encoder import EncoderConfig
from features.UI.Encoder.encoder import RotaryEncoder


from features.logger.logger import Logger

class EncoderFactory(Factory):
    def __init__(self, logger: Logger = None):
        super().__init__("ui", logger)

    def create(self):
        config = EncoderConfig(self.config)

        return RotaryEncoder(config)