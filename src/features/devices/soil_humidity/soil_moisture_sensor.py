from features.devices.device import Device, DeviceConfig, ADCTopic
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from features.analog_accessor.analog_accessor import AnalogAccessor
from features.devices.soil_humidity.drivers.default import SMSDriver
from features.devices.soil_humidity.drivers.gravity_v1 import GravityV1
from utime import ticks_ms
import uasyncio


# TODO introduce locks

class Moisture(ADCTopic):
    pass

# Enum
class PlantState:
    DRY_WARNING = 0
    FLOWERING = 1
    NORMAL = 2

class SoilMoistureSensor(Device):
    FLOWERING_TRESHOLD = 30
    FLOWERING_DETECTION_TRESHOLD = 10

    def __init__(self, mqtt: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger,
                 analog_accessor: AnalogAccessor):
        super().__init__(mqtt, config, logger)
        data = config.config

        self._moisture = Moisture(mqtt, data["moisture"], logger)
        self._loop_span_ms = data["loopSpanMs"]
        self._sensor = self._create_sensor(analog_accessor, data["channel"])

        self._prev_moisture_val = -1
        self._moisture_val = 0
        self._moisture_unit = data["moisture"]["unit"]

        self._plant_state = PlantState.NORMAL

    def _create_sensor(self, analog_accessor: AnalogAccessor, channel: int):
        if self.config.name == "gravity_v1":
            return GravityV1(analog_accessor, channel)

        return SMSDriver(analog_accessor, channel)

    async def _update_config(self):
        pass

    async def _loop(self):
        # initial prev
        if self._prev_moisture_val < 0:
            self._prev_moisture_val = await self._sensor.read()
        
        current_time = ticks_ms()
        self._moisture_val = await self._sensor.read()


        if abs(self._moisture_val - self._prev_moisture_val) >= SoilMoistureSensor.FLOWERING_DETECTION_TRESHOLD:
            self._plant_state = PlantState.FLOWERING
            print("flowering")
        elif self._moisture_val <= SoilMoistureSensor.FLOWERING_TRESHOLD:
            self._plant_state = PlantState.DRY_WARNING
            print("dry warning")
        else:
            self._plant_state = PlantState.NORMAL



        self._moisture.update(self.base_topic, current_time, self._moisture_val)
        self.logger.debug(f"Moisture: {self._moisture_val}.")

        await uasyncio.sleep_ms(self._loop_span_ms)

    # For dynamic polling from UI Thread
    async def get_moisture(self):
        return self._moisture_val, self._moisture_unit

    async def get_plant_state(self):
        return self._plant_state