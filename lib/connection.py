import urequests as requests
import ujson as json
import utils
import uos as os
import network
from pin import onboard_led
import time

def send_api_request(base_url, path, headers={}, data={}):
    auth_variables = utils.retrieve_auth_variables(utils.join_path(os.getcwd(), "env.json"))
    if headers:
        auth_variables.update(headers)
    if data:
        data = json.dumps(data)
        auth_variables['Content-Type'] = 'application/json'
        return json.loads(requests.post(url= base_url + path + "/", headers=auth_variables, data=data).content)
    return json.loads(requests.get(url= base_url + path + "/", headers=auth_variables).content)

def connect_to_wifi(wlan_variables):
    # Attempt to connect to WIFI
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wlan_variables["SSID"], wlan_variables["PASSWORD"])
    print(f"Attempting to connect to {wlan_variables['SSID']}")
    while not wlan.isconnected():
        onboard_led()
        time.sleep(0.5)
        onboard_led()
        time.sleep(0.5)
    print("WLAN Connected")
    return wlan

def test_connection(url):
    try:
        status = requests.get(url=url).status_code
        if status == 200:
            return True
        return False
    except:
        return False

