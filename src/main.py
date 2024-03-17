import sys
import gc

from application import App
from features.logger.logger import Logger
from features.logger.logger_levels import LoggerLevels
from features.mqtt.mqtt_factory import MqttFactory
from features.network.connection_factory import ConnectionFactory

from utime import sleep
from machine import reset


def setup_fail(logger: Logger, message: str, error_code: int):
    logger.log_error(message)
    sys.exit(error_code)


if __name__ == '__main__':
    gc.collect()

    logger = Logger(LoggerLevels.DEBUG)

    connection = ConnectionFactory(logger).create()
    connection_result = connection.connect()
    if not connection_result:
        setup_fail(logger, f"Failed to connect with {connection.config.type}.", 1)

    mqtt = MqttFactory(logger).create()
    mqtt_connection_result = mqtt.connect()

    if not mqtt_connection_result:
        setup_fail(logger, f"Failed to connect with {mqtt.config.type}.", 2)

    app = App(logger)
    # topic configurations: {base_mqtt_topic}/{device_type}/{device_name}/{device_id}/{topic}
    #                           (optional)     (required)    (required)   (required)  (required)
    app.start()
