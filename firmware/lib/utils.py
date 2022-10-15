import ujson as json


def retrieve_auth_variables(auth_path):
    """
    Open and JSON load authorization variables, all stuff contained in secrets.json

    params:

        auth_path(str): string of path that will be opened and json loaded.
    """
    try:
        with open(auth_path) as open_auth:
            return json.load(open_auth)
    except:
        return None


def auth_variables_valid(loaded_auth):
    """
    Determines whether the loaded secrets.json values contain all necessary values

    params:
        loaded_auth(loaded json): json object imported into python that contains the secrets values
    """
    if not loaded_auth:
        return False
    ssids = loaded_auth.get("SSIDS_PASSWORD")
    base_url = loaded_auth.get("BASE_URL")
    auth = loaded_auth.get("AUTHORIZATION")
    if not ssids or not base_url or not auth:
        return False
    return True


def get_base_path(path):
    """
    Helper function to retun base path e.g. test/best/rest -> test/best

    params:
        path(str): str representation of path check above for example
    """
    split_path = path.split("/")
    return "/".join(split_path[0:-1])


def join_path(*args):
    """
    Takes a bunch of args, and joins them together to form a path

    params:
        args: all parts of the path e.g. join_path(test,best,rest) returns "test/best/rest"
    """
    path_list = list(args)
    return "/".join(path_list)

class partial:

    """
    Method used to pass a function/method with parameters but delay execution till called. Useful for storing functions in a list.

    params:

        func(function): Function you wish to delay calling
        args:(args): Any arguments you wish to pass to the function
        kwargs:(kwargs): Any keyword arguments you wish to pass to the function
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwds):
        return self.func(*self.args, *args, **kwds, **self.kwargs)