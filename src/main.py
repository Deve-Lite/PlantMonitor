import sys
import gc

from application import App
from features.devices.device import DeviceConfig
from features.devices.device_factory import DeviceFactory
from features.logger.logger import Logger
from features.logger.logger_levels import LoggerLevels
from features.mqtt.mqtt_factory import MqttFactory
from features.network.connection_factory import ConnectionFactory

from utime import sleep
from machine import reset
from ujson import loads

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

    # topic configurations: {base_mqtt_topic}/{device_type}/{device_name}/{device_id}/{topic}
    #                           (optional)     (required)    (required)   (required)  (required)

    mqtt = MqttFactory(logger).create()
    mqtt_connection_result = mqtt.connect()

    if not mqtt_connection_result:
        setup_fail(logger, f"Failed to connect with {mqtt.config.type}.", 2)

    path = "configuration/devices.json"
    logger.log_info(f"Reading configuration from: {path}")
    with open(path, 'r') as file:
        json_file = file.read()
    device_configurations = loads(json_file)

    if len(device_configurations) == 0:
        setup_fail(logger, "No devices found in configuration file.", 3)
        sleep(5)

    devices = []
    device_factory = DeviceFactory(mqtt, logger)
    for device_config in device_configurations:
        config = DeviceConfig(device_config)
        device = device_factory.create(config)
        devices.append(device)

    app = App(logger)
    app.start()
