import sys
import gc
import uasyncio
import ntptime

from application import App
from features.analog_accessor.analog_accessor_factory import AnalogAccessorFactory
from features.devices.device_factory import DeviceFactory
from features.logger.logger import Logger
from features.logger.logger_levels import LoggerLevels
from features.mqtt.mqtt_factory import MqttFactory
from features.network.connection_factory import ConnectionFactory

from utime import sleep, localtime, gmtime
from machine import reset


def setup_fail(logger: Logger, message: str, error_code: int):
    logger.log_error(message)
    sleep(5)
    sys.exit(error_code)
    # in release change to reset()


if __name__ == '__main__':
    gc.collect()

    logger = Logger(LoggerLevels.ERROR)

    connection = ConnectionFactory(logger).create()
    connection_result = connection.connect()
    if not connection_result:
        setup_fail(logger, f"Failed to connect with {connection.config.type}.", 1)

    logger.log_info("Synchronizing time with ntptime module")
    ntptime.settime()
    logger.log_info(f"Global time: {gmtime()}")

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


