from features.analog_accessor.analog_accessor import AnalogAccessor
from features.devices.drivers.adc_driver import AnalogDriver
from math import log, e


class GravityV1(AnalogDriver):
    def __init__(self, analog_accessor: AnalogAccessor, channel: int):
        super().__init__(analog_accessor, channel)
        self.wet = 23000
        self.mid = 37000
        self.dry = 50000

    async def _read(self):
        raw = await self.read_raw()

        if raw >= self.dry:
            return 0
        if raw <= self.wet:
            return 100

        calc = int(1246.17 - 115.51 * log(raw, e))

        return min(100, max(0, calc))
