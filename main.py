from lib.pin import button_one, button_two, button_three, button_four, button_five, button_six, button_seven, button_eight
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

button_one = button_one()
button_two = button_two()
button_three = button_three()
button_four = button_four()
button_five = button_five()
button_six = button_six()
button_seven = button_seven()
button_eight = button_eight()

while True:
    if button_one.value():
        baby_scout.left_breast(baby_scout.children[0])
    if button_two.value():
        baby_scout.breast_feed(baby_scout.children[0])
    if button_three.value():
        baby_scout.right_breast(baby_scout.children[0])
    if button_four.value():
        baby_scout.bottle_feed(baby_scout.children[0])
    if button_five.value():
        baby_scout.wet_diaper(baby_scout.children[0])
    if button_six.value():
        baby_scout.solid_diaper(baby_scout.children[0])
    if button_seven.value():
        baby_scout.wet_solid_diaper(baby_scout.children[0])
    if button_eight.value():
        baby_scout.sleep(baby_scout.children[0])




#baby1 = babyscout.children[0]
#babyscout.bottle_feed(baby1)
#time.sleep(1)
#babyscout.bottle_feed(baby1)
