import gc
import asyncio
import ntptime
import json
from application import App
from logger.logger import Logger
from time import gmtime
from machine import Pin, reset
from utils.network import setup_network
from utils.utils import blink

DEBUG = True
LED_PIN = 8
SETTINGS_FILE = 'appsettings.json'

def list_networks(self):
    wlan = network.WLAN(network.STA_IF)
    networks = wlan.scan()

    self.logger.debug("Networks found: {}".format(len(networks)))
    self.logger.debug("-------------------------------------------")
    for wlan in networks:
        self.logger.debug("SSID: {}".format(wlan[0].decode('utf-8')))
        self.logger.debug("BSSID: {}".format(':'.join(['%02x' % b for b in wlan[1]])))
        self.logger.debug("Channel: {}".format(wlan[2]))
        self.logger.debug("RSSI: {}".format(wlan[3]))
        self.logger.debug("Authmode: {}".format(wlan[4]))
        self.logger.debug("Hidden: {}".format(wlan[5]))
        self.logger.debug("-------------------------------------------")

async def main():
    logger = Logger(DEBUG)
    try:
        gc.collect()

        logger.info('Initializing device.')

        logger.debug(f"Free memory: {gc.mem_free()} bytes.")
        gc.collect()
        logger.debug(f"Free memory after collect: {gc.mem_free()} bytes.")
        
        led = Pin(LED_PIN, Pin.OUT)
        led.value(0)
        await asyncio.sleep_ms(500)
        await blink(led, 1)
        
        logger.info('Initializing Networn and Mqtt.')
        with open(SETTINGS_FILE) as f:
            config = json.load(f)
        
        mqtt_client = setup_network(config, logger)
        await blink(led, 1)

        logger.info("Synchronizing time with ntptime module")
        ntptime.settime()
        logger.info(f"Global time: {gmtime()}")
        await blink(led, 1)

        app = App(mqtt_client, logger, config)
        
        await app.start()
        
        logger.error("Application exited.")
        await blink(led, 5)
        await asyncio.sleep(1)
        
    except Exception as e:
        logger.error("Failed to start the application.")
        await blink(led, 5)
        await asyncio.sleep(1)
        
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        logger = Logger(DEBUG)
        logger.error("Failed to start the application.")
    finally:
        asyncio.new_event_loop()
        if not DEBUG:
            reset()