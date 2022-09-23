class Request:
    def __init__(self, request):
        self.raw = request
        self.method = None
        self.path = None
        self.protocol = None
        self.headers = None
        self.body = None
        self.parse_request()

    def parse_request(self):
        request, self.body = self.raw.split("\r\n\r\n")
        split_request = request.split("\r\n")
        request_line = split_request.pop(0)
        self.method, self.path, self.protocol = request_line.split(" ")
        headers = {}
        for header in split_request:
            key, value = header.split(": ")
            headers[key] = value
        self.headers = headers

        



