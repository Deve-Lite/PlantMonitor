import asyncio
import dht
import time
import sys
from logger.logger import Logger
from mqtt_as import MQTTClient
from machine import Pin, ADC

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
    sleep_ms = cfg["sleep"]

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
            
            async with lock:
                now = time.time() * 1000  # ms timestamp

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

        await asyncio.sleep_ms(sleep_ms)
        

async def soil_humidity_loop(logger: Logger, mqtt: MQTTClient, lock: asyncio.Lock, configuration: dict):
    cfg = configuration["humidity"]
    pin = cfg["pin"]

    base_topic = configuration["mqtt"]["baseTopic"]
    topic_soil = f"{base_topic}/{cfg['topic']}"
    topic_hum = f"{base_topic}/{cfg['topic']}/{cfg['humidity']['topic']}"
    hum_threshold = cfg["humidity"]["threshold"]
    hum_min_interval = cfg["humidity"]["min_interval"]
    sleep_ms = cfg["sleep"]

    logger.info(f"Soil humidity topic: {topic_soil}")
    logger.info(f"Soil humidity sensor topic: {topic_hum}")

    adc = ADC(Pin(pin))

    # Detect platform and set ADC range
    if sys.platform == "rp2":
        max_adc = 65535  # 16-bit for RP2040
    elif sys.platform == "esp32":
        adc.atten(ADC.ATTN_11DB)  # Configure full range
        max_adc = 4095  # 12-bit for ESP32
    else:
        max_adc = 4095  # Default to 12-bit

    last_hum = None
    last_hum_time = 0

    while True:
        try:
            raw_value = adc.read_u16() if sys.platform == "rp2" else adc.read()
            norm = raw_value / max_adc

            # Apply custom logic: dry if above ~85% of max
            if norm >= 3500 / 4095:
                humidity_percent = 0
            else:
                humidity_percent = int((1 - (norm / (3500 / 4095))) * 100)
                humidity_percent = max(0, min(100, humidity_percent))

            now = time.time() * 1000  # ms timestamp

            send_hum = (
                last_hum is None or
                abs(humidity_percent - last_hum) >= hum_threshold
            ) and (now - last_hum_time >= hum_min_interval)

            if send_hum:
                last_hum = humidity_percent
                last_hum_time = now
                async with lock:
                    await mqtt.publish(topic_hum, str(humidity_percent))
                    logger.info(f"Published soil humidity: {humidity_percent}%")

                    payload = {
                        "humidity": humidity_percent,
                        "timestamp": now
                    }
                    await mqtt.publish(topic_soil, str(payload))
                    logger.info(f"Published combined soil humidity data: {payload}")

        except Exception as e:
            logger.error(f"Error reading soil humidity sensor: {e}")

        await asyncio.sleep_ms(sleep_ms)


async def disconnection_worker(logger: Logger, mqtt: MQTTClient):
    logger.info("Starting mqtt disconnection worker.")
    
    try:
        while True:
            await mqtt.down.wait()
            mqtt.down.clear()
            logger.error("Wifi or broker connection is down.")
    except Exception as e:
        logger.error(f"Error in disconnection worker: {e}")

async def connection_worker(logger: Logger, mqtt: MQTTClient):
    logger.info("Starting mqtt connection worker.")
    try:
        while True:
            await mqtt.up.wait()
            mqtt.up.clear()
            logger.info("Connection established subscribing to topics.")
    except Exception as e:
        logger.error(f"Error in connection worker: {e}")

class App:
    def __init__(self, mqtt: MQTTClient, logger: Logger, configuration: dict):
        self._configuration = configuration
        self._mqtt = mqtt
        self._logger = logger
        self._lock = asyncio.Lock()

    async def start(self):
        
        self._logger.debug(f"Starting dht loop.")
        message = asyncio.create_task(dht_loop(self._logger, self._mqtt, self._lock, self._configuration))

        self._logger.debug(f"Starting soil humidity loop.")
        device = asyncio.create_task(soil_humidity_loop(self._logger, self._mqtt, self._lock, self._configuration))

        self._logger.debug(f"Starting disconnection worker.")
        disconnection = asyncio.create_task(disconnection_worker(self._logger, self._mqtt))
        
        self._logger.debug(f"Starting connection worker.")
        connection = asyncio.create_task(connection_worker(self._logger, self._mqtt))

        await asyncio.gather(message, device, disconnection, connection)


