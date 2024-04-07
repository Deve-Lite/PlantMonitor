from features.devices.device import Device, DeviceConfig, Topic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff, time
from ujson import dumps, loads
from features.analog_accessor.analog_accessor import AnalogAccessor
import machine
from drivers.sms import SMSDriver
import uasyncio


class Moisture(Topic):
    pass


class SoilMoistureSensor(Device):
    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger,
                 analog_accessor: AnalogAccessor):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._moisture = Moisture(mqtt, data["moisture"])
        self.loop_span_ms = data["loopSpanMs"]
        channel = data["channel"]
        self._sensor = SMSDriver(analog_accessor, channel)



    async def _update_config(self):
        pass

    async def _loop(self):
        self.logger.log_info(f"Internal loop of Soil moisture sensor.")
        
        
        current_time = ticks_ms()
        self._sensor.measure()

        moisture = self._sensor.moisture()

        self._moisture.update(self.base_topic, current_time, moisture)
        self.logger.log_debug(f"Moisture: {moisture}.")

        await uasyncio.sleep_ms(self.loop_span_ms)


