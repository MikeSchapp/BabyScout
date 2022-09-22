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
        self.init_children()

    def init_children(self):
        path = "children"
        children = send_api_request(self.base_url, path)["results"]
        for child in children:
            self.children.append(child["id"])

    def send_data(self, child_id, activity, data={}):
        path = activity
        data["child"] = child_id
        send_api_request(self.base_url, path, data=data)

    def resolve_timers(self, child_id, activity, data={}):
        current_timer = self.get_timer(child_id, activity)
        if current_timer:
            path = activity
            data["timer"] = current_timer["id"]
            send_api_request(self.base_url, path, data=data)
        else:
            self.set_timer(child_id, activity)

    def set_timer(self, child_id, activity):
        path = "timers"
        timer = send_api_request(
            self.base_url, path=path, data={"child": child_id, "name": activity}
        )
        return timer

    def get_timer(self, child_id, activity):
        path = "timers"
        timer_response = send_api_request(self.base_url, path=path)
        timers = timer_response.get("results", [])
        for timer in timers:
            if (
                timer["name"] == activity
                and timer["child"] == child_id
                and timer["active"] == True
            ):
                return timer
        return None

    def sleep(self, child_id):
        activity = "sleep"
        self.resolve_timers(child_id, activity)

    def tummy_time(self, child_id):
        activity = "tummy-times"
        self.resolve_timers(child_id, activity)

    def wet_diaper(self, child_id):
        activity = "changes"
        data = {"wet": True, "solid": False}
        self.send_data(child_id, activity, data)
        print("Recorded Diaper Change")

    def solid_diaper(self, child_id):
        activity = "changes"
        data = {"wet": False, "solid": True}
        self.send_data(child_id, activity, data)
        print("Recorded Diaper Change")

    def wet_solid_diaper(self, child_id):
        activity = "changes"
        data = {"wet": True, "solid": True}
        self.send_data(child_id, activity, data)
        print("Recorded Diaper Change")

    def breast_feed(self, child_id):
        activity = "feedings"
        data = {"type": "breast milk", "method": "both breasts"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Breast Feeding")

    def left_breast(self, child_id):
        activity = "feedings"
        data = {"type": "breast milk", "method": "left breast"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Breast Feeding")

    def right_breast(self, child_id):
        activity = "feedings"
        data = {"type": "breast milk", "method": "right breast"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Breast Feeding")

    def bottle_feed(self, child_id):
        activity = "feedings"
        data = {"type": "breast milk", "method": "bottle"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Bottle Feeding")


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
    print("Connected to BabyBuddy")
    return baby_buddy
