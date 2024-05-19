from features.devices.device import Device, DeviceConfig, ADCTopic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms


from features.devices.light.drivers.default import InsolationDriver
import uasyncio



class Insolation(ADCTopic):
    pass


class InsolationSensor(Device):
    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._insolation = Insolation(mqtt, data["insolation"], logger)
        self._loop_span_ms = data["loopSpanMs"]
        pin = data["adcPin"]
        
        self._sensor = InsolationDriver(pin)
        self._insolation_val = 0
        self._insolation_unit = data["insolation"]["unit"]

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()
        self._insolation_val = await self._sensor.read()

        # TODO remove
        #if self.get_lcd_status() is True:
        #    self.lcd.print_values(insolation, self._insolation_unit)
            

        self._insolation.update(self.base_topic, current_time, self._insolation_val)
        self.logger.debug(f"Insolation: {self._insolation_val}.")
        await uasyncio.sleep_ms(self._loop_span_ms)


    # for dynamic polling from UI thread
    async def get_insolation(self):
        return self._insolation_val, self._insolation_unit
        
