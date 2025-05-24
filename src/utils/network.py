import json
from logger.logger import Logger
from mqtt_as import config, MQTTClient

def setup_network(configuration: dict, logger: Logger):
    
    logger.debug(f"MQTT options: {configuration["mqtt"]["username"]}, {configuration["mqtt"]["password"]}, {configuration["mqtt"]["server"]}")

    config['server'] = configuration["mqtt"]["server"]
    config['port'] = configuration["mqtt"]["port"]
    
    config['client_id'] = configuration["mqtt"]["clientId"]
    config['user'] = configuration["mqtt"]["username"]
    config['password'] = configuration["mqtt"]["password"]
    
    config['ssl'] = configuration["mqtt"]["ssl"]
    config['ssl_params'] = {"server_hostname": configuration["mqtt"]["server"] }
    
    config["queue_len"] = 1
    config['clean'] = True
    config['keepalive'] = configuration["mqtt"]["keepAlive"]
    
    logger.debug(f"Wifi options: {configuration["network"]["ssid"]}, {configuration["network"]["password"]}")

    config['ssid'] = configuration["network"]["ssid"]
    config['wifi_pw'] = configuration["network"]["password"]

    if logger.is_debug:
        MQTTClient.DEBUG = True
    
    last_will_topic = f"{configuration["mqtt"]["baseTopic"]}/{configuration["mqtt"]["will"]["topic"]}"
    
    payload = {
        "online": False
    }
    last_will_message = json.dumps(payload)
    
    config["last_will"] = [last_will_topic, last_will_message, True, 0]

    return MQTTClient(config)
