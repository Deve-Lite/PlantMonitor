from features.analog_accessor.analog_accessor import AnalogAccessor
from features.devices.soil_humidity.drivers.default import SMSDriver
from features.devices.drivers.adc_driver import AnalogDriver
from math import log, e


class GravityV1(AnalogDriver):
    def __init__(self, analog_accessor: AnalogAccessor, channel: int):
        super().__init__(analog_accessor, channel)
        self.wet = 23000
        self.mid = 37000
        self.dry = 50000

    def _calculate(self, val):
        return 1246.17 - 115.51 * log(val, e)
