from features.devices.device import Device, DeviceConfig, ADCTopic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff, time
from ujson import dumps, loads
from features.analog_accessor.analog_accessor import AnalogAccessor
import machine
from drivers.insolation import InsolationDriver
import uasyncio


class Insolation(ADCTopic):
    pass


class InsolationSensor(Device):
    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger,
                 analog_accessor: AnalogAccessor):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._insolation = Insolation(mqtt, data["insolation"], logger)
        self.loop_span_ms = data["loopSpanMs"]
        channel = data["channel"]
        
        self.sensor = InsolationDriver(analog_accessor, channel)

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()
        await self.sensor.measure()

        insolation = 100 - self.sensor.insolation()
        self._insolation.update(self.base_topic, current_time, insolation)

        self.logger.debug(f"Insolation: {insolation}.")

        await uasyncio.sleep_ms(self.loop_span_ms)


