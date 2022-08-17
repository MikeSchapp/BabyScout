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
            self.timers[child["id"]] = []

    def resolve_timers(self, child_id, activity, data={}):
        if self.timers.get(child_id):
            path = activity
            timer =  self.timers[child_id][0]
            data["timer"] = timer["timer_id"]
            if timer["activity"] == activity:
                send_api_request(self.base_url, path, data=data)
            else:
                send_api_request(path, data=data)
                self.set_timer(child_id, activity)
        else: 
            self.set_timer(child_id, activity)


    def set_timer(self, child_id, activity):
        path = "timers"
        timer = self.send_api_request(self.base_url, path=path, data={'child': child_id})
        self.timers[child_id].append({"activity": activity, "timer_id": timer["id"]})
        return timer

    def sleep(self, child_id):
        activity = "sleep"
        self.resolve_timers(child_id, activity)

    def tummy_time(self, child_id):
        activity = "tummy-times"
        self.resolve_timers(child_id, activity)

    def breast_feed(self, child_id):
        activity = "feedings"
        data = {
            "type": "breast milk",
            "method": "both breasts"
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