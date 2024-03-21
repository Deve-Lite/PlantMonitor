from abstractions.factory import MultiFactory
from features.accessor.analog_accessor import AnalogAccessorConfig, AnalogAccessor


class AccessorFactory(MultiFactory):
    def __init__(self, logger):
        super().__init__("accessors", logger)
        self.max_items = 3

    def _create_item(self, config):
        config = AnalogAccessorConfig(config)

        if config.type == "HP4067":
            return AnalogAccessor(config, self.logger)

        raise NotImplementedError(f"Device {config.type} is not supported")
