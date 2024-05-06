from features.devices.device import Device
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient

from machine import reset
from utime import sleep

import uasyncio


async def message_loop(logger: Logger, mqtt: BaseMqttClient):
    while True:
        mqtt.update()
        await uasyncio.sleep(1)


class App:
    def __init__(self, mqtt: BaseMqttClient, devices: [], logger: Logger):
        self._mqtt = mqtt
        self._logger = logger
        self._devices = devices

    def reset_devices(self):
        self._logger.info("Resetting device.")
        sleep(1)
        reset()

    async def start(self):

        self._mqtt.subscribe("reset", self.reset_devices)

        message = uasyncio.create_task(message_loop(self._logger, self._mqtt))

        self._logger.debug(f"Starting devices loop: {len(self._devices)}")

        for device in self._devices:
            device_task = uasyncio.create_task(device.loop())

        await uasyncio.gather(message)

