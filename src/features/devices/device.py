from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff
from ujson import dumps
import uasyncio


class Topic:
    def __init__(self, mqtt: BaseMqttClient, config):
        self.mqtt = mqtt
        self.config = config
        self.unit = config["unit"]
        self.topic = config["topic"]
        self.sendAsJson = config["sendAsJson"]

        config = config["threshold"]
        self.type = config["type"]
        self.value = config["value"]
        self.minimalIntervalSeconds = config["minimalIntervalSeconds"]

        self._value = None
        self._last_update = ticks_ms()

    def update(self, base_topic: str, current_time, current_value):
        if abs(ticks_diff(current_time, self._last_update)) < self.minimalIntervalSeconds:
            return False

        if abs(current_value - self.value) == 0:
            return False

        self._last_update = current_time
        self._value = current_value

        topic = f"{base_topic}/{self.topic}"
        message = self.format_data()

        self.mqtt.publish(topic, message)

        return True

    def format_data(self):
        if not self.sendAsJson:
            return self._value

        json = {
            "unit": self.unit,
            "value": self._value,
            "time": self._last_update
        }

        return dumps(json)


class Availability:
    def __init__(self, config):
        self.enabled = config["availability"]["enabled"]
        self.topic = config["availability"]["topic"]


class DeviceConfig:
    def __init__(self, config):
        self.config = config["data"]
        self.id = config["id"]
        self.vcc = config["vcc"]
        self.ground = config["ground"]
        self.type = config["type"]
        self.name = config["name"]
        self.availability = Availability(config)


class Device:
    def __init__(self, mqtt_client: BaseMqttClient, config: DeviceConfig, logger: Logger):
        self.config = config
        self.mqtt = mqtt_client
        self.logger = logger
        self.base_topic = f"{self.config.type}/{self.config.name}/{self.config.id}/"

    async def _loop(self):
        raise NotImplementedError("Method not implemented")

    async def _update_config(self):
        # For reading states of other devices
        raise NotImplementedError("Method not implemented")

    async def loop(self):
        while True:
            try:
                await self._update_config()
                if self.config.availability.enabled:
                    await self._loop()
                else:
                    self.logger.log_info(f"Device {self.config.id} is disabled. Sleeping 500 ms.")
                    await uasyncio.sleep_ms(500)

            except Exception as e:
                self.logger.log_error(f"Device loop failed: {e}")
