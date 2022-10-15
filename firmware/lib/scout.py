from lib import utils
import urequests as requests
import ujson as json
import uos as os


class Scout:
    """
    Object for handling interactions with BabyBuddy Instance

    params:

        base_url(str): url that points to the babybuddy api e.g. 192.168.1.20:32000/api/
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.children = []
        self.init_children()
        self.child_index = None

    def init_children(self):
        """
        Since children can be assigned numbers that may not be sequential, find and store them for later.
        Creates a list of children ids
        """
        path = "children"
        children = send_api_request(self.base_url, path)["results"]
        for child in children:
            self.children.append(child["id"])

    def send_data(self, child_id, activity, data={}):
        """
        Method for sending api request for specific activities for a specific child

        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
            activity(str): String identifier of the activity being performed
            data(dict): Dictionary containing extra information e.g. timers etc.

        """
        path = activity
        data["child"] = child_id
        send_api_request(self.base_url, path, data=data)

    def resolve_timers(self, child_id, activity, data={}):
        """
        Check to see if a current timer is running, if not send request to start timer

        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
            activity(str): String identifier of the activity being performed
            data(dict): Dictionary containing extra information e.g. timers etc.
        """
        current_timer = self.get_timer(child_id, activity)
        if current_timer:
            path = activity
            data["timer"] = current_timer["id"]
            send_api_request(self.base_url, path, data=data)
        else:
            self.set_timer(child_id, activity)

    def set_timer(self, child_id, activity):
        """
        Call that instantiates a new timer

        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
            activity(str): String identifier of the activity being performed
        """
        path = "timers"
        timer = send_api_request(
            self.base_url, path=path, data={"child": child_id, "name": activity}
        )
        return timer

    def get_timer(self, child_id, activity):
        """
        Returns all active timers that match a given activity type

        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
            activity(str): String identifier of the activity being performed
        """
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
        """
        Start or end a sleep activity for a given child
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "sleep"
        self.resolve_timers(child_id, activity)

    def tummy_time(self, child_id):
        """
        Start or end a tummy_time activity for a given child
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "tummy-times"
        self.resolve_timers(child_id, activity)

    def wet_diaper(self, child_id):
        """
        Log wet diaper for a given child
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "changes"
        data = {"wet": True, "solid": False}
        self.send_data(child_id, activity, data)
        print("Recorded Diaper Change")

    def solid_diaper(self, child_id):
        """
        Log solid diaper for a given child
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "changes"
        data = {"wet": False, "solid": True}
        self.send_data(child_id, activity, data)
        print("Recorded Diaper Change")

    def wet_solid_diaper(self, child_id):
        """
        Log wet and solif diaper for a given child
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "changes"
        data = {"wet": True, "solid": True}
        self.send_data(child_id, activity, data)
        print("Recorded Diaper Change")

    def breast_feed(self, child_id):
        """
        Start or end timer for breasfeeding, specifically for both breasts
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "feedings"
        data = {"type": "breast milk", "method": "both breasts"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Breast Feeding")

    def left_breast(self, child_id):
        """
        Start or end timer for breasfeeding, specifically for left breast
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "feedings"
        data = {"type": "breast milk", "method": "left breast"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Breast Feeding")

    def right_breast(self, child_id):
        """
        Start or end timer for breasfeeding, specifically for right breast
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "feedings"
        data = {"type": "breast milk", "method": "right breast"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Breast Feeding")

    def bottle_feed(self, child_id):
        """
        Start or end timer for bottlefeeding, specifically for breast milk in bottle
        params:
            child_id(int): ID corresponding to child you wish to perform a specific action for
        """
        activity = "feedings"
        data = {"type": "breast milk", "method": "bottle"}
        self.resolve_timers(child_id, activity, data)
        print("Recorded Bottle Feeding")

    def next_child(self):
        """
        Method that allows stepping to the next child in list, or returning back to the start
        """
        if len(self.children) == 0:
            raise IndexError("No children setup in BabyBuddy")
        if self.child_index == None:
            self.child_index = 0
            return self.children[0]
        max_index = len(self.children) - 1
        new_index = self.child_index + 1
        if new_index > max_index:
            new_index = 0
        self.child_index = new_index
        return self.children[new_index]

    def previous_child(self):
        """
        Method that allows stepping to the previous child in list, or returning back to the end
        """
        if len(self.children) == 0:
            raise IndexError("No children setup in BabyBuddy")
        if self.child_index == None:
            self.child_index = len(self.children) - 1 
            return self.children[self.child_index]
        new_index = self.child_index - 1
        if new_index < 0:
            new_index = len(self.children) - 1 
        self.child_index = new_index
        return self.children[new_index]

def connect_to_baby_buddy(base_url):
    """
    Ensure that connectivity can be established to BabyBuddy instance
    """
    baby_buddy_reachable = False
    while not baby_buddy_reachable:
        try:
            baby_buddy = Scout(base_url)
            baby_buddy_reachable = True
        except OSError:
            print("Failed to connect to BabyBuddy")
    print("Connected to BabyBuddy")
    return baby_buddy


def send_api_request(base_url, path, headers={}, data={}):
    """
    Function used to send api requests to BabyBuddy Instance

    params:

        base_url(str): URL that points to BabyBuddy API
        path(str): Or activity to hit the correct api endpoint
        headers(dict): Contains necessary authorization headers
        data(dict): All data necessary to complete a api post request
    """
    auth_variables = utils.retrieve_auth_variables(
        utils.join_path(os.getcwd(), "../secrets.json")
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
