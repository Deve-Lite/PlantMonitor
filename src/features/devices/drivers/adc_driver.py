from features.analog_accessor.analog_accessor import AnalogAccessor


class AnalogDriver:
    def __init__(self, analog_accessor: AnalogAccessor, channel: int):
        self.analog_accessor = analog_accessor
        self.channel = channel
        self.min = 0
        self.max = 65535

    async def read_raw(self):
        return await self.analog_accessor.read(self.channel)

    async def read(self):
        return await self._read()

    async def _read(self):
        raw = await self.read_raw()

        if raw <= self.min:
            return 0
        if raw >= self.max:
            return 100

        calc = int(raw / self.max * 100)

        return min(100, max(0, calc))
