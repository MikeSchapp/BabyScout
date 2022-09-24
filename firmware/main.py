from lib.pin import create_button, onboard_led
import lib.scout as scout
import time
import uos as os
import ujson as json
import _thread
from lib.utils import retrieve_auth_variables, join_path, auth_variables_valid
from lib.connection import (
    connect_to_access_point,
    scan_access_points,
    access_point_nearby,
    access_point_wifi_setup
)
from lib.webpage import config_route, default_route
from lib.scout import connect_to_baby_buddy
from lib.webrouter import WebRouter

# Retrieve WLAN Variables from secrets.json and establish connectivity to WLAN and BabyScout

# Case when secrets.json does not exist
ap_mode = False

WLAN_VARIABLES = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))
local_access_points = scan_access_points()
if auth_variables_valid(WLAN_VARIABLES):
    nearby_matching_access_point = access_point_nearby(local_access_points, WLAN_VARIABLES.get("SSIDS_PASSWORD").keys())
    if nearby_matching_access_point:
        WLAN = connect_to_access_point(
            nearby_matching_access_point,
            WLAN_VARIABLES["SSIDS_PASSWORD"][nearby_matching_access_point],
        )
        BABY_SCOUT = connect_to_baby_buddy(base_url=WLAN_VARIABLES["BASE_URL"])
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
    else:
        ap_mode = True
else:
    ap_mode = True
if ap_mode:
    print("No matching wifi, falling back to webpage based setup.")
    ap = access_point_wifi_setup()
    ip = ap.ifconfig()[0]
    app = WebRouter(ip, 80, default_route)
    app.route("/config")(config_route)()
    app.serve()