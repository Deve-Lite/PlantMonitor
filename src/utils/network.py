from logger.logger import Logger
from mqtt_as import config, MQTTClient

def setup_network(configuration: dict, logger: Logger):
    
    logger.debug(f"MQTT options: {configuration["mqtt"]["username"]}, {configuration["mqtt"]["password"]}, {configuration["mqtt"]["server"]}")

    config['user'] = configuration["mqtt"]["username"]
    config['password'] = configuration["mqtt"]["password"]
    config['server'] = configuration["mqtt"]["server"]
    config['ssl'] = configuration["mqtt"]["ssl"]
    config['ssl_params'] = {"server_hostname": configuration["mqtt"]["server"] }
    config["queue_len"] = 1
    
    logger.debug(f"Wifi options: {configuration["network"]["ssid"]}, {configuration["network"]["password"]}")

    config['ssid'] = configuration["network"]["ssid"]
    config['wifi_pw'] = configuration["network"]["password"]

    if logger.is_debug:
        MQTTClient.DEBUG = True

    return MQTTClient(config)