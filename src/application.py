from features.devices.device import Device
from features.logger.logger import Logger
from features.mqtt.mqtt import BaseMqttClient

from utime import sleep

import uasyncio
import _thread
import gc

def message_loop(logger: Logger, mqtt: BaseMqttClient):
    while True:
        try:
            mqtt.update()
            sleep(1)
            gc.collect()
        except Exception as e:
            logger.log_error(f"Error in message loop: {e}")
            sleep(1)
            raise e


class App:
    def __init__(self, mqtt: BaseMqttClient, devices: [Device], logger: Logger):
        self._mqtt = mqtt
        self._logger = logger
        self._devices = devices

    async def start(self):
        _thread.start_new_thread(message_loop, (self._logger, self._mqtt))

        self._logger.log_debug("Starting device loop.")
        for device in self._devices:
            uasyncio.create_task(device.loop())

        while True:
            await uasyncio.sleep(10)
            self._logger.log_debug("Main loop working.")
