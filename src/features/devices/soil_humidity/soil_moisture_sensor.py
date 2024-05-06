from features.devices.device import Device, DeviceConfig, ADCTopic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from features.analog_accessor.analog_accessor import AnalogAccessor
from features.devices.soil_humidity.drivers.default import SMSDriver
from features.devices.soil_humidity.drivers.gravity_v1 import GravityV1
from utime import ticks_ms
import uasyncio


class Moisture(ADCTopic):
    pass


class SoilMoistureSensor(Device):
    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger,
                 analog_accessor: AnalogAccessor):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._moisture = Moisture(mqtt, data["moisture"], logger)
        self.loop_span_ms = data["loopSpanMs"]
        self.sensor = self._create_sensor(analog_accessor, data["channel"])

    def _create_sensor(self, analog_accessor: AnalogAccessor, channel: int):
        if self.config.name == "gravity_v1":
            return GravityV1(analog_accessor, channel)

        return SMSDriver(analog_accessor, channel)

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()
        moisture = await self.sensor.read()

        self._moisture.update(self.base_topic, current_time, moisture)
        self.logger.debug(f"Moisture: {moisture}.")

        await uasyncio.sleep_ms(self.loop_span_ms)


