from lib.pin import create_button, onboard_led
import lib.scout as scout
import time
import uos as os
from lib.utils import retrieve_auth_variables, join_path
from lib.connection import connect_to_wifi
from lib.scout import connect_to_baby_buddy

wlan_variables = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))
BASE_URL = wlan_variables["BASE_URL"]
connect_to_wifi(wlan_variables=wlan_variables)
baby_scout = connect_to_baby_buddy(base_url=BASE_URL)
# Set default to first child in BabyBuddy, add functionality to allow for toggling between multiple children.
child = baby_scout.children[0]


# Create button matrix, matching gpio pin to the specific action you want to capture
button_gpio_pins = [9,8,7,6,5,4,3,2]
buttons = []
button_actions = [
    baby_scout.left_breast,
    baby_scout.breast_feed,
    baby_scout.right_breast,
    baby_scout.bottle_feed,
    baby_scout.wet_diaper,
    baby_scout.solid_diaper,
    baby_scout.wet_solid_diaper,
    baby_scout.sleep
]
for button in button_gpio_pins:
    buttons.append(create_button(button))



while True:
    for index, button in enumerate(buttons):
        if button.value():
            onboard_led(1)
            time.sleep(0.5)
            onboard_led(0)
            button_actions[index](child)





#baby1 = babyscout.children[0]
#babyscout.bottle_feed(baby1)
#time.sleep(1)
#babyscout.bottle_feed(baby1)
