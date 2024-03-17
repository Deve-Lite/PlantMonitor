from features.devices.device import Device, DeviceConfig, Topic, Threshold
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient

from utime import ticks_ms, ticks_diff
import ujson
import machine
import dht


class DHT11Config:
    def __init__(self, config):
        device_data = config["data"]
        self.data_pin = device_data["pin"]
        self.temperature = Topic(device_data["temperature"])
        self.humidity = Topic(device_data["humidity"])


class DHT11(Device):
    DHT_READ_SPAN = 2000

    def __init__(self, mqtt_client: BaseMqttClient,
                 config: DeviceConfig,
                 logger: Logger):
        super().__init__(mqtt_client, config, logger)
        self._device_config = DHT11Config(config.config)
        dht_pin = machine.Pin(self._device_config.data_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._sensor = dht.DHT11(dht_pin)
        self._humidity = None
        self._temp = None
        self._last_read = ticks_ms()

    async def _update_config(self):
        pass

    async def _loop(self):
        current_time = ticks_ms()
        if abs(ticks_diff(current_time, self._last_read)) < DHT11.DHT_READ_SPAN:
            return

        self._last_read = current_time
        self.logger.log_info("Starting loop of dht11 sensor.")
        self._sensor.measure()
        temp = self._sensor.temperature()
        humidity = self._sensor.humidity()

        self.logger.log_debug(f"Measured temp: {temp}, hum: {humidity}.")

        if self.push_next or self._should_update_temp(temp) or self._should_update_humidity(humidity):
            self.logger.log_debug(f"Updating dht11 data.")
            payload = self._create_payload(temp, humidity)
            topic = self.device_config.topic
            self.mqtt_client.publish(topic, payload)
            self.push_next = False


    def get_subscriptions(self):
        actions = [
            (self.__generate_topic("temp"), self.__update_temp)
        ]

        return actions

    def __generate_topic(self, topic):
        return f"{self.config.base_device_topic}{self.device_config.update_topic}{topic}"

    def __update_temp(self, data, logger):
        logger.log_debug("Updating temp with data")
        data = ujson.loads(data)

        if "type" in data and data["type"] == "temp":
            if "value" in data and data["value"] >= 1:
                self.device_config.temp_threshold.value = data["value"]

            if "unit" in data and data["unit"] == "C" or data["unit"] == "K" or data["unit"] == "F":
                self.device_config.temp_threshold.unit = data["unit"]

    def _should_update_humidity(self, humidity):
        if self._humidity is None:
            self._humidity = humidity
            return True

        if self.device_config.hum_threshold.type == "percent":
            if abs(self._humidity - humidity) > self.device_config.hum_threshold.value:
                self._humidity = humidity
                return True

        return False

    def _should_update_temp(self, temp):
        if self._temp is None:
            self._temp = temp
            return True

        if self.device_config.temp_threshold.type == "degrees":
            if abs(self._temp - temp) > self.device_config.temp_threshold.value:
                self._temp = temp
                return True

        return False

    def _create_payload(self, temp, humidity):
        temp_unit = self.device_config.temp_threshold.unit
        self.logger.log_debug(f"DHT11 temp unit: {temp_unit}")

        if temp_unit == "F":
            temp = self.celsius_to_fahrenheit(temp)
        elif temp_unit == "K":
            temp = self.celsius_to_kelvin(temp)

        self.logger.log_debug(f"Updated temp: {temp}")

        data = {
            "device": self.device_config.id,
            "temperature": {
                "value": temp,
                "unit": temp_unit
            },
            "humidity": {
                "value": humidity,
                "unit": self.device_config.hum_threshold.unit
            }
        }

        self.logger.log_debug(f"Formatted payload: {data}")

        return ujson.dumps(data)

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return fahrenheit

    @staticmethod
    def celsius_to_kelvin(celsius):
        kelvin = celsius + 273.15
        return kelvin
