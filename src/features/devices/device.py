from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient

import uasyncio


class Threshold:
    def __init__(self, config):
        self.config = config
        self.type = config["type"]
        self.value = config["value"]
        self.minimalIntervalSeconds = config["minimalIntervalSeconds"]


class Topic:
    def __init__(self, config):
        self.config = config
        self.unit = config["unit"]
        self.topic = config["topic"]
        self.sendAsJson = config["sendAsJson"]
        self.threshold = Threshold(config["threshold"])


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
        self.client = mqtt_client
        self.logger = logger

    async def _loop(self):
        raise NotImplementedError("Method not implemented")

    async def _update_config(self):
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
