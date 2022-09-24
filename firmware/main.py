from lib.pin import create_button, onboard_led
import lib.scout as scout
import time
import uos as os
import _thread
from lib.utils import retrieve_auth_variables, join_path
from lib.connection import (
    connect_to_access_point,
    scan_access_points,
    access_point_nearby,
    access_point_wifi_setup
)
from lib.webpage import load_webpage
from lib.scout import connect_to_baby_buddy
from lib.webrouter import WebRouter

# Retrieve WLAN Variables from secrets.json and establish connectivity to WLAN and BabyScout

def default_route(*args, **kwargs):
    return load_webpage("lib/webpages/default.html")

def config_route(*args, **kwargs):
    return load_webpage("lib/webpages/config.html")


WLAN_VARIABLES = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))
BASE_URL = WLAN_VARIABLES["BASE_URL"]
nearby_matching_access_point = access_point_nearby(scan_access_points(), WLAN_VARIABLES)
if nearby_matching_access_point:
    WLAN = connect_to_access_point(
        nearby_matching_access_point,
        WLAN_VARIABLES["SSIDS_PASSWORD"][nearby_matching_access_point],
    )
else:
    print("No matching wifi, falling back to webpage based setup")
    ap = access_point_wifi_setup()
    ip = ap.ifconfig()[0]
    app = WebRouter(ip, 80, default_route)
    app.route("/test")(config_route)()
    app.serve()


BABY_SCOUT = connect_to_baby_buddy(base_url=BASE_URL)
# Set default to first child in BabyBuddy, add functionality to allow for toggling between multiple children.
child = BABY_SCOUT.children[0]

# Create button matrix, matching gpio pin to the specific action you want to capture
button_gpio_pins = [9, 8, 7, 6, 5, 4, 3, 2]
button_actions = [
    BABY_SCOUT.left_breast,
    BABY_SCOUT.breast_feed,
    BABY_SCOUT.right_breast,
    BABY_SCOUT.bottle_feed,
    BABY_SCOUT.wet_diaper,
    BABY_SCOUT.solid_diaper,
    BABY_SCOUT.wet_solid_diaper,
    BABY_SCOUT.sleep,
]

# Initialize buttons
buttons = []
for button in button_gpio_pins:
    buttons.append(create_button(button))


# Loop through and check if any button has been pressed.


def button_pressed():
    while True:
        for index, button in enumerate(buttons):
            if button.value():
                onboard_led(1)
                time.sleep(0.5)
                onboard_led(0)
                button_actions[index](child)


# Continually check and assure connectivity to wireless and babyscout


def ensure_connection():
    global WLAN
    global BABY_SCOUT
    while True:
        print("Testing Connection")
        if not WLAN.isconnected():
            print("Lost Connection")
            WLAN = connect_to_access_point(wlan_variables=WLAN_VARIABLES)
            print("Reconnected")
        time.sleep(10)


# Start thread to ensure internet connection
_thread.start_new_thread(ensure_connection, ())

# Begin button checking loop
button_pressed()

