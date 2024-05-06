from features.devices.drivers.adc_driver import AnalogDriver
from math import log, e
from machine import Pin, ADC
from uasyncio import sleep_ms


class InsolationDriver(AnalogDriver):
    def __init__(self, adc_pin: int):
        self.adc = ADC(Pin(adc_pin))
        self.light = 1000
        self.dark = 50000

    async def read_raw(self):
        await sleep_ms(1)
        return self.adc.read_u16()

    async def _read(self):
        raw = await self.read_raw()

        if raw >= self.dark:
            return 0
        if raw <= self.light:
            return 100

        calc = int(276.295 - 24.188 * log(raw, e))

        return min(100, max(0, calc))
