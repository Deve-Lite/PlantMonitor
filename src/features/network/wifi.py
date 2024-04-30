from features.logger.logger import Logger
from features.network.connection import Connection, ConnectionConfiguration

from utime import sleep

import network


class WiFi(Connection):
    def __init__(self, logger: Logger, config: ConnectionConfiguration):
        super().__init__(logger, config)
        self._wlan = network.WLAN(network.STA_IF)

    def is_connected(self):
        return self._wlan.isconnected()

    def connect(self):
        self.logger.info(f"Connecting to ssid {self.config.ssid}.")
        self.logger.debug(f"Ssid: {self.config.ssid}, Password: {self.config.password}")

        self._wlan.active(True)
        self._wlan.connect(self.config.ssid, self.config.password)

        sleep(1)
        i = 0
        while not self._wlan.isconnected() and i < 15:
            status = self._wlan.status()
            self.logger.warning(f"""Not Connected. Status: {status},
             means {self.get_status_description(status)}""")
            i += 1
            sleep(1)

        status = self._wlan.status()
        status_description = self.get_status_description(status)

        if not self._wlan.isconnected():
            self.logger.warning(f"Not Connected. Status: {status}, means {status_description}.")
            return False

        self.logger.info(f"Connected. Status: {status}, means {status_description}.")
        return True

    @staticmethod
    def get_status_description(status):
        if status == network.STAT_IDLE:
            return "No connection and no activity"
        elif status == network.STAT_CONNECTING:
            return "Connecting in progress"
        elif status == network.STAT_WRONG_PASSWORD:
            return "Failed due to incorrect password"
        elif status == network.STAT_NO_AP_FOUND:
            return "Failed because no access point replied"
        elif status == network.STAT_CONNECT_FAIL:
            return "Failed due to other problems"
        elif status == network.STAT_GOT_IP:
            return "Connection successful"
        return "Unknown"