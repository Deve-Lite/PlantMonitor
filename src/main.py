import sys
import gc
import uasyncio
import ntptime

from application import App
from features.analog_accessor.analog_accessor_factory import AnalogAccessorFactory
from features.devices.device_factory import DeviceFactory
from features.logger.file_logger import FileLogger
from features.logger.logger import Logger
from features.mqtt.mqtt_factory import MqttFactory
from features.network.connection_factory import ConnectionFactory

from utime import sleep, localtime, gmtime
from machine import reset


def setup_fail(logger: Logger, message: str, error_code: int):
    logger.error(message)
    logger.error(str(error_code))
    sleep(5)
    reset()


if __name__ == '__main__':
    gc.collect()

    logger = FileLogger(console=True, debug=False)

    connection = ConnectionFactory(logger).create()
    connection_result = connection.connect()
    if not connection_result:
        setup_fail(logger, f"Failed to connect with {connection.config.type}.", 1)

    logger.info("Synchronizing time with ntptime module")
    ntptime.settime()
    logger.info(f"Global time: {gmtime()}")

    mqtt = MqttFactory(logger).create()
    mqtt_connection_result = mqtt.connect()

    if not mqtt_connection_result:
        setup_fail(logger, f"Failed to connect with {mqtt.config.type}.", 2)

    accessor_factory = AnalogAccessorFactory(logger)
    accessors = accessor_factory.create()

    device_factory = DeviceFactory(mqtt, accessors, logger)
    devices = device_factory.create()

    app = App(mqtt, devices, logger)
    uasyncio.run(app.start())


