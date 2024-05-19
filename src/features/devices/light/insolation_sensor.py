from features.devices.device import Device, DeviceConfig, ADCTopic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms
from features.analog_accessor.analog_accessor import AnalogAccessor

from features.devices.light.drivers.default import InsolationDriver
import uasyncio


from features.UI.LCD.lcd import MyLCD

class Insolation(ADCTopic):
    pass


class InsolationSensor(Device):
    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger,
                 lcd: MyLCD):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._insolation = Insolation(mqtt, data["insolation"], logger)
        self.loop_span_ms = data["loopSpanMs"]
        pin = data["adcPin"]
        
        self.sensor = InsolationDriver(pin)
        self.lcd = lcd
        self._insolation_unit = data["insolation"]["unit"]

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()
        insolation = await self.sensor.read()

        if self.get_lcd_status() is True:
            self.lcd.print_values(insolation, self._insolation_unit)
            

        self._insolation.update(self.base_topic, current_time, insolation)
        self.logger.debug(f"Insolation: {insolation}.")
        await uasyncio.sleep_ms(self.loop_span_ms)
