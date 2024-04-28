from abstractions.factory import MultiFactory
from features.analog_accessor.analog_accessor import AnalogAccessor
from features.logger.logger import Logger
from features.devices.air.dht11 import DHT11
from features.devices.light.insolation_sensor import InsolationSensor
from features.devices.soil_humidity.soil_moisture_sensor import SoilMoistureSensor
from features.devices.device import DeviceConfig
from features.mqtt.mqtt import BaseMqttClient



class DeviceFactory(MultiFactory):
    def __init__(self, client: BaseMqttClient, analog_accessors: [], logger: Logger):
        super().__init__("devices", logger)
        self.logger = logger
        self.client = client
        self.analog_accessors = analog_accessors
        self.max_items = 48

    def _create_item(self, config):
        config = DeviceConfig(config)

        if config.type == "air":
            if config.name == "dht11":
                return DHT11(self.client, config, self.logger)
            raise NotImplementedError("Air device is not supported")

        if config.type == "soil":
            if config.name == "sms":

                mux_id = config.config["mux_id"]
                accessor = self.find_analog_accessor(mux_id)

                return SoilMoistureSensor(self.client, config, self.logger, accessor)

        if config.type == "light":
            if config.name == "is":

                mux_id = int(config.config["mux_id"])
                accessor = self.find_analog_accessor(mux_id)

                return InsolationSensor(self.client, config, self.logger, accessor)

        raise NotImplementedError(f"Device {config.type}-{config.name} is not supported")

    def find_analog_accessor(self, mux_id):
        for accessor in self.analog_accessors:
            if int(accessor.config.id) == mux_id:
                return accessor
        
        print("HEEEEEJ")
        raise ValueError(f"There isn't any analog accessor with id {mux_id}")
