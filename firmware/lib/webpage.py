def load_webpage(location):
    with open(location, "r") as website:
        webpage = website.read()
    return webpage