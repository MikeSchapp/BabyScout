import lib.scout as scout
import time
import uos as os
from pin import onboard_led
from lib.utils import retrieve_auth_variables, join_path
from lib.connection import connect_to_wifi
from lib.scout import connect_to_baby_buddy

wlan_variables = retrieve_auth_variables(join_path(os.getcwd(), "secrets.json"))
BASE_URL = wlan_variables["BASE_URL"]
connect_to_wifi(wlan_variables=wlan_variables)
connect_to_baby_buddy(base_url=BASE_URL)

#baby1 = babyscout.children[0]
#babyscout.bottle_feed(baby1)
#time.sleep(1)
#babyscout.bottle_feed(baby1)
