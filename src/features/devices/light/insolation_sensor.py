from features.devices.device import Device, DeviceConfig, Topic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff, time
from ujson import dumps, loads
from features.analog_accessor.analog_accessor import AnalogAccessor
import machine
from drivers.insolation import InsolationDriver
import uasyncio


class Insolation(Topic):
    pass


class InsolationSensor(Device):
    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger,
                 analog_accessor: AnalogAccessor):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._insolation = Insolation(mqtt, data["insolation"])
        self.loop_span_ms = data["loopSpanMs"]
        channel = data["channel"]
        
        self._sensor = InsolationDriver(analog_accessor, channel)

        


    async def _update_config(self):
        pass

    async def _loop(self):
        self.logger.log_info(f"Internal loop of Insolation sensor.")
       
        current_time = ticks_ms()
        self._sensor.measure()

        insolation = self._sensor.insolation()
        self._insolation.update(self.base_topic, current_time, insolation)
       

        self.logger.log_debug(f"Insolation: {insolation}.")

        await uasyncio.sleep_ms(self.loop_span_ms)


