from features.analog_accessor.analog_accessor import AnalogAccessor

class SMSDriver:
    def __init__(self, analog_accessor: AnalogAccessor, channel, min_moist=0, max_moist=65535):
        self.analog_accessor  = analog_accessor
        self.moisture_val = -1
        self.channel = channel
        self.min_moist = min_moist
        self.max_moist = max_moist

    async def measure(self):
        val = await self.analog_accessor.read(self.channel)
        self.moisture_val = val

    def moisture(self):
        if self.moisture_val < 0:
            raise RuntimeError("moisture() method called before measure()")
        return int((self.moisture_val - self.min_moist) * 100 / (self.max_moist - self.min_moist))

    