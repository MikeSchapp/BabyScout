import uos as os
import ujson as json
import machine


def load_webpage(location):
    with open(location, "r") as website:
        webpage = website.read()
    return webpage


def default_route(*args, **kwargs):
    return load_webpage("lib/webpages/default.html")


def config_route(*args, **kwargs):
    request = kwargs.get("request")
    if request.query_strings:
        if "secrets.json" in os.listdir():
            with open("secrets.json", "r+") as secret:
                secret_json = json.loads(secret.read())
            with open("secrets.json", "w") as secret:
                secret_json["SSIDS_PASSWORD"][
                    request.query_strings["ssid"]
                ] = request.query_strings["password"]
                secret.write(json.dumps(secret_json))
        else:
            with open("secrets.json", "w") as secret:
                secret_json["SSIDS_PASSWORD"][
                    request.query_strings["ssid"]
                ] = request.query_strings["password"]
                secret_json["AUTHORIZATION"]["Authorization"] = (
                    "Token " + request.query_strings["babyauth"]
                )
                secret.write(json.dumps(secret_json))
    machine.reset()
