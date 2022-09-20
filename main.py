from lib.pin import create_button, onboard_led
import lib.scout as scout
import time
import uos as os
import _thread
from lib.utils import retrieve_auth_variables, join_path
from lib.connection import connect_to_wifi, test_connection
from lib.scout import connect_to_baby_buddy

WLAN_VARIABLES = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))
BASE_URL = WLAN_VARIABLES["BASE_URL"]
WLAN = connect_to_wifi(wlan_variables=WLAN_VARIABLES)
BABY_SCOUT = connect_to_baby_buddy(base_url=BASE_URL)

# Set default to first child in BabyBuddy, add functionality to allow for toggling between multiple children.
child = BABY_SCOUT.children[0]

# Create button matrix, matching gpio pin to the specific action you want to capture
button_gpio_pins = [9,8,7,6,5,4,3,2]
button_actions = [
    BABY_SCOUT.left_breast,
    BABY_SCOUT.breast_feed,
    BABY_SCOUT.right_breast,
    BABY_SCOUT.bottle_feed,
    BABY_SCOUT.wet_diaper,
    BABY_SCOUT.solid_diaper,
    BABY_SCOUT.wet_solid_diaper,
    BABY_SCOUT.sleep
]

#Initialize buttons
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
            WLAN = connect_to_wifi(wlan_variables=WLAN_VARIABLES)
            print("Reconnected")
        time.sleep(10)

        
# Start thread to ensure internet connection
_thread.start_new_thread(ensure_connection, ())

# Begin button checking loop
button_pressed()

