import network
from lib.pin import onboard_led
import time


class PicoConnection:
    def __init__(self):
        self.wlan = self.wireless_client_setup()
        self.nearby_access_points = self.scan_access_points()

    @staticmethod
    def wireless_client_setup():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        return wlan

    @staticmethod
    def access_point_wifi_setup():
        ap = network.WLAN(network.AP_IF)
        ap.config(essid="BabyScout", password="BabyBuddy")
        ap.active(True)
        print(ap.status())
        print(ap)
        return ap

    def connect_to_access_point(self, ssid, password):
        # Attempt to connect to WIFI
        if ssid not in self.nearby_access_points:
            return False
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        print(f"Attempting to connect to {ssid}")
        while not self.wlan.isconnected():
            onboard_led()
            time.sleep(0.5)
            onboard_led()
            time.sleep(0.5)
        print("WLAN Connected")
        return True

    def scan_access_points(self):
        nearby_access_point_list = []
        nearby_access_points = self.wlan.scan()
        for ssid in nearby_access_points:
            nearby_access_point_list.append(ssid[0].decode("utf-8"))
        self.wlan.active(False)
        while "" in nearby_access_point_list:
            nearby_access_point_list.remove("")
        print(nearby_access_point_list)
        return nearby_access_point_list

    def access_point_nearby(self, configured_ssids):
        matching_ssids = []
        for ssid in configured_ssids:
            if ssid in self.nearby_access_points:
                matching_ssids.append(ssid)
        if matching_ssids:
            return matching_ssids[0]
        return None
