import lib.scout as scout
import time
import uos as os
import network
from pin import onboard_led
from lib.utils import retrieve_auth_variables, join_path

wlan_variables = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))
BASE_URL = wlan_variables["BASE_URL"]

# Attempt to connect to WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wlan_variables["SSID"], wlan_variables["PASSWORD"])
while not wlan.isconnected():
    print(f"Attempting to connect to {wlan_variables["SSID"]}")
    onboard_led()
    time.sleep(0.5)
    onboard_led()
    time.sleep(0.5)
    print(wlan.isconnected())
    
# Attempt to establish connection to BabyBuddy Instance
baby_buddy_reachable = False
while not baby_buddy_reachable:
    try:
        babyscout = scout.Scout(BASE_URL)
        baby_buddy_reachable = True
    except OSError:
        print("Failed to connect to BabyBuddy")
        onboard_led()
        time.sleep(1)
        onboard_led()

onboard_led(0)
#baby1 = babyscout.children[0]
#babyscout.bottle_feed(baby1)
#time.sleep(1)
#babyscout.bottle_feed(baby1)
