import urequests as requests
import ujson as json
import utils
import uos as os
import network
from pin import onboard_led
import time


def send_api_request(base_url, path, headers={}, data={}):
    auth_variables = utils.retrieve_auth_variables(
        utils.join_path(os.getcwd(), "secrets.json")
    )["AUTHORIZATION"]
    if headers:
        auth_variables.update(headers)
    if data:
        data = json.dumps(data)
        auth_variables["Content-Type"] = "application/json"
        return json.loads(
            requests.post(
                url=base_url + path + "/", headers=auth_variables, data=data
            ).content
        )
    return json.loads(
        requests.get(url=base_url + path + "/", headers=auth_variables).content
    )

def scan_access_points():
    nearby_access_point_list = []
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    nearby_access_points = wlan.scan()
    for ssid in nearby_access_points:
       nearby_access_point_list.append(ssid[0].decode('utf-8'))
    wlan.active(False)
    return nearby_access_point_list

def access_point_nearby(nearby_ssids, wlan_variables):
    matching_ssids = []
    for ssid in wlan_variables["SSIDS_PASSWORD"].keys():
        if ssid in nearby_ssids:
            matching_ssids.append(ssid)
    if matching_ssids:
        return matching_ssids[0]
    return None

def connect_to_access_point(ssid, password):
    # Attempt to connect to WIFI
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(f"Attempting to connect to {ssid}")
    while not wlan.isconnected():
        onboard_led()
        time.sleep(0.5)
        onboard_led()
        time.sleep(0.5)
    print("WLAN Connected")
    return wlan

def access_point_wifi_setup():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid="BabyScout", password="BabyBuddy")
    ap.ifconfig(('192.168.0.2', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
    ap.active(True)
    return ap


def test_connection(url):
    try:
        status = requests.get(url=url).status_code
        if status == 200:
            return True
        return False
    except:
        return False

