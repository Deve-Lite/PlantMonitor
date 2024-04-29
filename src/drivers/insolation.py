from features.analog_accessor.analog_accessor import AnalogAccessor


class InsolationDriver:
    def __init__(self, analog_accessor: AnalogAccessor, channel, min_insolation=0, max_insolation=65535):
        self.analog_accessor  = analog_accessor
        self.insolation_val = -1
        self.channel = channel
        self.min_insolation = min_insolation
        self.max_insolation = max_insolation

    async def measure(self):
        val = await self.analog_accessor.read(self.channel)
        self.insolation_val = val


    def insolation(self):
        if self.insolation_val < 0:
            raise RuntimeError("insolation() method called before measure()", self.insolation_val)
        return int((self.insolation_val - self.min_insolation) * 100 / (self.max_insolation - self.min_insolation))

    