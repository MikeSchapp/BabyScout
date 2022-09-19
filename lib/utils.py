import ujson as json

def retrieve_auth_variables(auth_path):
    with open(auth_path) as open_auth:
        return json.load(open_auth)

def get_base_path(path):
    split_path = path.split("/")
    return "/".join(split_path[0:-1])

def join_path(*args):
    path_list = list(args)
    return "/".join(path_list)
