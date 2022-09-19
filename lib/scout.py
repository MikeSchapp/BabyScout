import urequests as requests
import ujson as json
import uos as os
import ussl as ssl
from micropython import *
from connection import send_api_request
from pin import onboard_led
import time

class Scout:
    def __init__(self, base_url):
        self.base_url = base_url
        self.children = []
        self.timers = {}
        self.init_children()

    def init_children(self):
        path = "children"
        children = send_api_request(self.base_url, path)["results"]
        for child in children:
            self.children.append(child["id"])
            self.timers[child["id"]] = {
                "feedings": None,
                "sleep": None
            }

    def send_data(self, child_id, activity, data={}):
        path = activity
        data['child'] = child_id
        send_api_request(self.base_url, path, data=data)


    def resolve_timers(self, child_id, activity, data={}):
        if self.timers[child_id].get(activity):
            path = activity
            timer =  self.timers[child_id][activity]
            data["timer"] = timer["timer_id"]
            send_api_request(self.base_url, path, data=data)
            self.timers[child_id][activity] = None
        else: 
            self.set_timer(child_id, activity)


    def set_timer(self, child_id, activity):
        path = "timers"
        timer = send_api_request(self.base_url, path=path, data={'child': child_id})
        self.timers[child_id][activity] = ({"activity": activity, "timer_id": timer["id"]})
        return timer

    def sleep(self, child_id):
        activity = "sleep"
        self.resolve_timers(child_id, activity)

    def tummy_time(self, child_id):
        activity = "tummy-times"
        self.resolve_timers(child_id, activity)

    def wet_diaper(self, child_id):
        activity = 'changes'
        data = {
            "wet": True,
            "solid": False
        }
        self.send_data(child_id, activity, data)

    def solid_diaper(self, child_id):
        activity = 'changes'
        data = {
            "wet": False,
            "solid": True
        }
        self.send_data(child_id, activity, data)

    def wet_solid_diaper(self, child_id):
        activity = 'changes'
        data = {
            "wet": True,
            "solid": True
        }
        self.send_data(child_id, activity, data)

    def breast_feed(self, child_id):
        activity = "feedings"
        data = {
            "type": "breast milk",
            "method": "both breasts"
        }
        self.resolve_timers(child_id, activity, data)

    def left_breast(self, child_id):
        activity = "feedings"
        data = {
            "type": "breast milk",
            "method": "left breast"
        }
        self.resolve_timers(child_id, activity, data)

    def right_breast(self, child_id):
        activity = "feedings"
        data = {
            "type": "breast milk",
            "method": "right breast"
        }
        self.resolve_timers(child_id, activity, data)

    def bottle_feed(self, child_id):
        activity = "feedings"
        data = {
            "type": "breast milk",
            "method": "bottle"
        }
        self.resolve_timers(child_id, activity, data)


def connect_to_baby_buddy(base_url):
# Attempt to establish connection to BabyBuddy Instance
    baby_buddy_reachable = False
    while not baby_buddy_reachable:
        try:
            baby_buddy = Scout(base_url)
            baby_buddy_reachable = True
        except OSError:
            print("Failed to connect to BabyBuddy")
            onboard_led()
            time.sleep(1)
            onboard_led()
    onboard_led(0)
    return baby_buddy