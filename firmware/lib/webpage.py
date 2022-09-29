import uos as os
import ujson as json
import machine
import template


def load_webpage(location):
    with open(location, "r") as website:
        webpage = website.read()
    return webpage


def default_route(*args, **kwargs):
    options = [
        {"ssid": "SSID:"},
        {"password": "Password:"},
        {"babybuddy": "BabyBuddy URL:"},
        {"babyauth": "BabyBuddy API Key"},
    ]
    render = ""
    for option in options:
        for key, value in option.items():
            render += f""" <input type="text" id="{key}" name="{key}" placeholder="{value}"><br><br>"""
    return template.render_template(
        load_webpage("webpages/default.html"), {"render": render}
    )


def config_route(*args, **kwargs):
    request = kwargs.get("request")
    secret_json = {}
    if request.query_strings:
        if "secrets.json" in os.listdir():
            with open("secrets.json", "r+") as secret:
                secret_json = json.loads(secret.read())
        with open("secrets.json", "w") as secret:
            secret_json["SSIDS_PASSWORD"] = {}
            secret_json["SSIDS_PASSWORD"][
                request.query_strings.get("ssid", "")
            ] = request.query_strings.get("password", "")
            if request.query_strings.get("babybuddy"):
                secret_json["BASE_URL"] = request.query_strings.get("babybuddy")
            if request.query_strings.get("babyauth"):
                if "AUTHORIZATION" not in secret_json.keys():
                    secret_json["AUTHORIZATION"] = {}
                secret_json["AUTHORIZATION"][
                    "Authorization"
                ] = request.query_strings.get("babyauth")
            secret.write(json.dumps(secret_json))
    machine.reset()
