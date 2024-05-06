import sys
import gc
import uasyncio
import ntptime

from application import App
from features.analog_accessor.analog_accessor_factory import AnalogAccessorFactory
from features.devices.device_factory import DeviceFactory
from features.logger.file_logger import FileLogger
from features.logger.logger_levels import LoggerLevels
from features.mqtt.mqtt_factory import MqttFactory
from features.network.connection_factory import ConnectionFactory

from utime import sleep, localtime, gmtime
from machine import reset, Pin


def setup_fail(logger: Logger, message: str, error_code: int):
    logger.error(message)
    sleep(5)
    sys.exit(error_code)
    # in release change to reset()


def blink():
    led.value(1)
    sleep(0.2)
    led.value(0)


if __name__ == '__main__':
    gc.collect()

    logger = FileLogger(console=True, debug=False)
    logger.info("Device starting")
    led = Pin(25, Pin.OUT)
    led.value(0)
    sleep(1)

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



