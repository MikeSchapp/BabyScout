import urequests as requests
import ujson as json
import uos as os
import ussl as ssl
from micropython import *
from lib.utils import retrieve_auth_variables, join_path

class Scout:
    def __init__(self, base_url):
        self.base_url = base_url
        self.children = []
        self.timers = {}
        self.init_children()

    def init_children(self):
        url = "children"
        children = self.send_api_request(url)["results"]
        for child in children:
            self.children.append(child["id"])
            self.timers[child["id"]] = []

        
    def send_api_request(self, path, headers={}, data={}):
        auth_variables = retrieve_auth_variables(join_path(os.getcwd(), "env.json"))
        if headers:
            auth_variables.update(headers)
        if data:
            data = json.dumps(data)
            auth_variables['Content-Type'] = 'application/json'
            return json.loads(requests.post(url= self.base_url + path + "/", headers=auth_variables, data=data).content)
        return json.loads(requests.get(url= self.base_url + path + "/", headers=auth_variables).content)

    def resolve_timers(self, child_id, activity, data={}):
        if self.timers.get(child_id):
            path = activity
            timer =  self.timers[child_id][0]
            data["timer"] = timer["timer_id"]
            if timer["activity"] == activity:
                self.send_api_request(path, data=data)
            else:
                self.send_api_request(path, data=data)
                self.set_timer(child_id, activity)
        else: 
            self.set_timer(child_id, activity)


    def set_timer(self, child_id, activity):
        path = "timers"
        timer = self.send_api_request(path=path, data={'child': child_id})
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
