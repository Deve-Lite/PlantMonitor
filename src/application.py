from features.devices.device import Device
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient

from utime import sleep

import uasyncio
import _thread
import gc


async def message_loop(logger: Logger, mqtt: BaseMqttClient):
    while True:
        mqtt.update()
        await uasyncio.sleep(1)


class App:
    def __init__(self, mqtt: BaseMqttClient, devices: [], logger: Logger):
        self._mqtt = mqtt
        self._logger = logger
        self._devices = devices

    async def start(self):
        message = uasyncio.create_task(message_loop(self._logger, self._mqtt))

        self._logger.log_debug(f"Starting devices loop: {len(self._devices)}")

        for device in self._devices:
            device_task = uasyncio.create_task(device.loop())

        await uasyncio.gather(message)

