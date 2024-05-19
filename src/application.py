from features.devices.device import Device
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient
from features.UI.Encoder.encoder import RotaryEncoder
from features.UI.ui import UI

from utime import sleep

import uasyncio
import _thread
import gc


async def message_loop(logger: Logger, mqtt: BaseMqttClient):
    while True:
        mqtt.update()
        await uasyncio.sleep(1)


class App:
    def __init__(self, mqtt: BaseMqttClient, devices: [], logger: Logger, ui: UI):
        self._mqtt = mqtt
        self._logger = logger
        self._devices = devices
        self._ui = ui

    async def start(self):
        message = uasyncio.create_task(message_loop(self._logger, self._mqtt))

        self._logger.debug(f"Starting devices loop: {len(self._devices)}")

        for device in self._devices:
            device_task = uasyncio.create_task(device.loop())

        gui_task = uasyncio.create_task(self._ui.loop())

        await uasyncio.gather(message)

