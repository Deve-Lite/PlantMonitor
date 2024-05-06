from features.analog_accessor.analog_accessor import AnalogAccessor
from features.devices.drivers.adc_driver import AnalogDriver
from math import log, e

class InsolationDriver(AnalogDriver):
    def __init__(self, analog_accessor: AnalogAccessor, channel: int):
        self.analog_accessor = analog_accessor
        self.channel = channel
        self.light = 25000
        self.mid = 33000
        self.dark = 50000

    def _calculate(self, val):
        calculated = 1162.08 - 105.507 * log(val, e)
        return min(100, max(0, int(calculated)))
