import asyncio
import dht
import time
from logger.logger import Logger
from mqtt_as import MQTTClient
from machine import Pin

async def dht_loop(logger: Logger, mqtt: MQTTClient, lock: asyncio.Lock, configuration: dict):
    cfg = configuration["dht"]
    pin = cfg["pin"]
    sensor_type = cfg.get("version", "dht22")

    # Extract topics once
    topic_dht = f"{configuration["mqtt"]["baseTopic"]}/{cfg["topic"]}"
    topic_temp = f"{configuration["mqtt"]["baseTopic"]}/{cfg["topic"]}/{cfg["temperature"]["topic"]}" 
    topic_hum = f"{configuration["mqtt"]["baseTopic"]}/{cfg["topic"]}/{cfg["humidity"]["topic"]}" 
    temp_threshold = cfg["temperature"]["threshold"]
    temp_min_interval = cfg["temperature"]["min_interval"]
    hum_threshold = cfg["humidity"]["threshold"]
    hum_min_interval = cfg["humidity"]["min_interval"]

    logger.info(f"Dht topic: {topic_dht}")
    logger.info(f"Dht temp. topic: {topic_temp}")
    logger.info(f"Dht hum. topic: {topic_hum}")

    # Select appropriate sensor class
    if sensor_type.lower() == "dht22":
        sensor = dht.DHT22(Pin(pin))
    else:
        sensor = dht.DHT11(Pin(pin))

    last_temp = None
    last_hum = None
    last_temp_time = 0
    last_hum_time = 0

    while True:
        try:
            sensor.measure()
            temperature = sensor.temperature()
            humidity = sensor.humidity()

            send_temp = False
            send_hum = False
            send_dht = False

            # Check temperature
            if (last_temp is None or
                abs(temperature - last_temp) >= temp_threshold) and \
                    (now - last_temp_time >= temp_min_interval):
                last_temp = temperature
                last_temp_time = now
                send_temp = True
                send_dht = True

            # Check humidity
            if (last_hum is None or
                abs(humidity - last_hum) >= hum_threshold) and \
                    (now - last_hum_time >= hum_min_interval):
                last_hum = humidity
                last_hum_time = now
                send_hum = True
                send_dht = True

            async with lock:
                now = time.time() * 1000  # ms timestamp
                
                if send_temp:
                    await mqtt.publish(topic_temp, str(temperature))
                    logger.info("Published temperature: {}".format(temperature))

                if send_hum:
                    await mqtt.publish(topic_hum, str(humidity))
                    logger.info("Published humidity: {}".format(humidity))

                if send_dht:
                    payload = {
                        "temperature": temperature,
                        "humidity": humidity,
                        "timestamp": now
                    }
                    await mqtt.publish(topic_dht, str(payload))
                    logger.info("Published combined dht: {}".format(payload))

        except Exception as e:
            logger.error("Error reading DHT sensor: {}".format(e))

        await asyncio.sleep_ms(500)


async def humidity_loop(logger: Logger, mqtt: MQTTClient, lock: asyncio.Lock, configuration: dict):
    pass

class App:
    def __init__(self, mqtt: MQTTClient, logger: Logger, configuration: dict):
        self._configuration = configuration
        self._mqtt = mqtt
        self._logger = logger
        self._lock = asyncio.Lock()

    async def start(self):
        
        self._logger.debug(f"Starting devices loop: {len(self._devices)}")
        message = asyncio.create_task(dht_loop(self._logger, self._mqtt, self._lock, self._configuration))

        self._logger.debug(f"Starting incoming messages loop: {len(self._devices)}")
        device = asyncio.create_task(humidity_loop(self._logger, self._mqtt, self._lock, self._configuration))

        await asyncio.gather(message, device)

