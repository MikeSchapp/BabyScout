from lib.pin import create_button, onboard_led
import time
import uos as os
import _thread
from lib.utils import retrieve_auth_variables, join_path, auth_variables_valid, partial
from picoconnection import PicoConnection
from lib.webpage import config_route, default_route
from lib.scout import connect_to_baby_buddy
from picowebrouter import WebRouter
import machine

# Retrieve WLAN Variables from secrets.json and establish connectivity to WLAN and BabyScout
WLAN_VARIABLES = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))

# Setup object for managing AP connections
pico_connection = PicoConnection()
ap_mode = False


if auth_variables_valid(WLAN_VARIABLES):
    nearby_matching_access_point = pico_connection.access_point_nearby(
        WLAN_VARIABLES.get("SSIDS_PASSWORD").keys()
    )
    if nearby_matching_access_point:
        onboard_led(1)
        pico_connection.connect_to_access_point(
            nearby_matching_access_point,
            WLAN_VARIABLES["SSIDS_PASSWORD"][nearby_matching_access_point],
        )
        onboard_led(0)
        BABY_SCOUT = connect_to_baby_buddy(base_url=WLAN_VARIABLES["BASE_URL"])
        # Set default to first child in BabyBuddy, add functionality to allow for toggling between multiple children.
        BABY_SCOUT.next_child()

        # Create button matrix, matching gpio pin to the specific action you want to capture
        button_gpio_pins = [9, 8, 7, 6, 5, 4, 3, 2]
        button_actions = [
            partial(BABY_SCOUT.left_breast, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.breast_feed, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.right_breast, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.bottle_feed, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.wet_diaper, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.solid_diaper, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.wet_solid_diaper, BABY_SCOUT.children[BABY_SCOUT.child_index]),
            partial(BABY_SCOUT.sleep, BABY_SCOUT.children[BABY_SCOUT.child_index])
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
                        try:
                            button_actions[index]()
                        except Exception as e:
                            print(f"Error: {e}")
                            # Continually check and assure connectivity to wireless and babyscout
                            print(f"Command failed to send, checking connection: {pico_connection.wlan.status()}")
                            if pico_connection.wlan.status() <= 0 or pico_connection.wlan.status() >= 3:
                                print("Lost connection, reconnecting...")
                                pico_connection.wlan.disconnect()
                                pico_connection.connect_to_access_point(
                                    nearby_matching_access_point,
                                    WLAN_VARIABLES["SSIDS_PASSWORD"][nearby_matching_access_point],
                                )
                                if pico_connection.wlan.status() == 3:
                                    print("Reconnected")
                                    button_actions[index]()
                                else: print("Failed to reconnect")

        # Begin button checking loop
        button_pressed()
    else:
        ap_mode = True
else:
    ap_mode = True
if ap_mode:
    # Start ap mode to allow for conffiguration of BabyScout via wifi access point.
    print("No matching wifi, falling back to webpage based setup.")
    ap = pico_connection.access_point_wifi_setup("BabyScout", "BabyBuddy")
    ip = ap.ifconfig()[0]
    app = WebRouter(ip, 80, default_route, "webpages/static")
    app.route("/config")(config_route)()
    app.serve()


