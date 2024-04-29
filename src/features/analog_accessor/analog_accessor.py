from features.devices.device import Device, DeviceConfig
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient

from machine import ADC, Pin

import uasyncio


class AnalogAccessorConfig:
    def __init__(self, config: {}):
        self.slots = config["slots"]
        self.adc_pin = config["adcPin"]
        self.pins = config["pins"]
        self.type = config["type"]
        self.id = config["id"]


class AnalogAccessor:
    def __init__(self, config: AnalogAccessorConfig, logger: Logger):
        self.logger = logger
        self.config = config

        self.adc = ADC(Pin(config.adc_pin))
        self.pins = [Pin(pin, Pin.OUT) for pin in self.config.pins]

        for pin in self.pins:
            pin.value(0)

        self.lock = uasyncio.Lock()

    async def read(self, channel: int):
        if channel < 0 or channel >= self.config.slots:
            return None

        try:
            await self.lock.acquire()

            self._apply_idx(channel)
            value = self.adc.read_u16()
            self.logger.debug(f"ADC value: {value}")

            return value
        except Exception as e:
            self.logger.error(f"Error reading value from ADC. Error: {e}")
            return None
        finally:
            self.lock.release()

    def _apply_idx(self, channel):
        self.pins[0].value(channel & 0x01)
        self.pins[1].value((channel >> 1) & 0x01)
        self.pins[2].value((channel >> 2) & 0x01)
        self.pins[3].value((channel >> 3) & 0x01)
