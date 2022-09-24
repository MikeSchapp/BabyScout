import ujson as json


def retrieve_auth_variables(auth_path):
    try:
        with open(auth_path) as open_auth:
            return json.load(open_auth)
    except:
        return None

def auth_variables_valid(loaded_auth):
    ssids = loaded_auth.get("SSIDS_PASSWORD")
    base_url = loaded_auth.get("BASE_URL")
    auth = loaded_auth.get("AUTHORIZATION")
    if not ssids or not base_url or not auth:
        return False
    return True

def get_base_path(path):
    split_path = path.split("/")
    return "/".join(split_path[0:-1])


def join_path(*args):
    path_list = list(args)
    return "/".join(path_list)
