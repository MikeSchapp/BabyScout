class Request:
    def __init__(self, request):
        self.raw = request
        self.method = None
        self.path = None
        self.query_strings = None
        self.protocol = None
        self.headers = None
        self.body = None
        self.parse_request()

    def parse_request(self):
        print(self.raw)
        try:
            request, self.body = self.raw.split("\r\n\r\n")
        except ValueError:
            request = self.raw
        split_request = request.split("\r\n")
        request_line = split_request.pop(0)
        self.method, self.path, self.protocol = request_line.split(" ")
        if "?" in self.path:
            query_strings = {}
            self.path, raw_query = self.path.split("?")
            raw_query = raw_query.split("&")
            for query in raw_query:
                key, value = query.split("=")
                query_strings[key] = value
            self.query_strings = query_strings

        headers = {}
        for header in split_request:
            key, value = header.split(": ")
            headers[key] = value
        self.headers = headers
