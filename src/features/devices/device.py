from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from utime import ticks_ms, ticks_diff, time
from ujson import dumps, loads
import uasyncio

MILISECONDS = 1000


class Topic:
    def __init__(self, mqtt: BaseMqttClient, config, logger: Logger):
        self.mqtt = mqtt
        self.config = config
        self.unit = config["unit"]
        self.topic = config["topic"]
        self.sendAsJson = config["sendAsJson"]

        config = config["threshold"]
        self.threshold_type = config["type"]
        self.threshold_value = config["value"]
        self.minimal_interval_seconds = config["minimalIntervalSeconds"]

        self._value = 0
        self._last_update = self.minimal_interval_seconds * MILISECONDS
        self._update_start_time = ticks_ms() - 60 * MILISECONDS
        self._update_span = 30

        self.logger = logger

    def update(self, base_topic: str, current_time, current_value):
        if abs(ticks_diff(current_time, self._last_update)) < self.minimal_interval_seconds * MILISECONDS:
            return False

        if abs(current_value - self._value) < self.threshold_value:
            self._update_start_time = None
            return False
        else:
            if self._update_start_time is None:
                self._update_start_time = current_time

            if abs(current_value - self._value) >= 2 * self.threshold_value:
                pass
            elif abs(ticks_diff(current_time, self._update_start_time)) < 60 * MILISECONDS:
                # Ensure that this is real change not temporary breeze etc.
                return False

        self._last_update = current_time
        self._value = current_value
        self._update_start_time = None

        topic = f"{base_topic}/{self.topic}"
        message = self.format_data()

        self.mqtt.publish(topic, message)
        self.logger.info(f"Published update on {topic}. Value: {self._value}.")

        return True

    def format_data(self):
        if not self.sendAsJson:
            return self._value

        json = {
            "value": self._value,
            "unit": self.unit,
            "time": time(),
            "timeUnit": "s"
        }

        return dumps(json)


class ADCTopic(Topic):
    def __init__(self, mqtt: BaseMqttClient, config, logger: Logger):
        super().__init__(mqtt, config, logger)
        self._update_start_time = ticks_ms() - 60 * MILISECONDS
        self._update_span = 60


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
        self.base_topic = f"{self.config.type}/{self.config.name}/{self.config.id}"
        availability_topic = f"{self.base_topic}/{self.config.availability.topic}"
        self.mqtt.subscribe(availability_topic, self._availability_switch)
        self._log_iterator = 0

    def _availability_switch(self, payload: str):
        if payload in ["on", "1"]:
            self.config.availability.enabled = True

        if payload in ["off", "0"]:
            self.config.availability.enabled = False

        if "value" not in payload:
            return

        data = loads(payload)
        value = data.get("value", None)

        if value is None:
            return

        if value in ["on", "1"]:
            self.config.availability.enabled = True

        if value in ["off", "0"]:
            self.config.availability.enabled = False

    async def _loop(self):
        raise NotImplementedError("Method not implemented")

    async def _update_config(self):
        # For reading states of other devices
        raise NotImplementedError("Method not implemented")

    async def loop(self):
        self.logger.info(f"Starting loop for device with Id: {self.config.id}")
        while True:
            try:
                self.logger.debug(f"Starting update config.")
                await self._update_config()
                self.logger.debug(f"Finished update config.")
                if self.config.availability.enabled:
                    self._log_iterator += 1
                    if self._log_iterator >= 20:
                        self._log_iterator = 0
                        self.logger.info(f"Sensor: {self.config.id} ({self.config.type}) is working.")
                    self.logger.debug(f"Starting internal loop.")
                    await self._loop()  # Device sleeps in this loop
                    self.logger.debug(f"Finished internal loop.")
                else:
                    await uasyncio.sleep_ms(500)
            except Exception as e:
                self.logger.error(f"Device {self.config.id} ({self.config.type}) loop failed: {e}")


