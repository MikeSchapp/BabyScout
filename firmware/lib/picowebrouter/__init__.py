from .objects.request import *
from .utils import walk_directories
import socket
import uos as os


class WebRouter:
    def __init__(self, ip, port, default, static_location="static"):
        self.routes = {"default": default}
        self.socket = self.open_socket(ip, port)
        self.static_location = static_location
        self.static_files = []
        self.add_static()

    def route(self, path):
        def router(function):
            def wrapper(*args, **kwargs):
                self.routes[path] = function

            return wrapper

        return router

    def add_static(self):
        static_files = walk_directories(self.static_location)
        if static_files:
            for directory in static_files.keys():
                for file in static_files[directory]:
                    self.static_files.append(f"{directory}/{file}")

    @staticmethod
    def open_socket(ip, port):
        address = (ip, port)
        new_socket = socket.socket()
        new_socket.bind((ip, port))
        new_socket.listen(1)
        return new_socket

    @staticmethod
    def determine_mimetype(path):
        mimetype = "text/html"
        if path.endswith(".js"):
            mimetype = "text/javascript"
        if path.endswith(".css"):
            mimetype = "text/css"
        return mimetype

    def serve(self):
        while True:
            client = self.socket.accept()[0]
            request = client.recv(1024)
            if request:
                request = Request(request.decode("utf-8"))
                path = request.path
                header = "HTTP/1.1 200 OK\n"
                mimetype = self.determine_mimetype(path)
                if path in self.routes.keys():
                    webpage = self.routes[path](request=request)
                elif path in self.static_files:
                    with open(path, "rb") as static:
                        webpage = static.read()
                else:
                    webpage = self.routes["default"](request=request)
                header += f"Content-Type: {mimetype}\n\n"
                client.sendall(webpage)
                client.close()

