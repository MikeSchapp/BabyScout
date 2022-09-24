from request import Request
import socket

class WebRouter:
    def __init__(self, ip, port, default):
        self.routes = {
            "default": default
        }
        self.socket = self.open_socket(ip, port)
    
    def route(self, path):
        def router(function):
            def wrapper(*args, **kwargs):
                self.routes[path] = function
            return wrapper
        return router
            

    @staticmethod
    def open_socket(ip, port):
        address = (ip, port)
        new_socket = socket.socket()
        new_socket.bind((ip, port))
        new_socket.listen(1)
        return new_socket

    def serve(self):
        while True:
            client = self.socket.accept()[0]
            request = client.recv(1024)
            request = Request(request.decode('utf-8'))
            path = request.path
            if path in self.routes.keys():
                webpage = self.routes[path](request=request)
            else:
                webpage = self.routes["default"](request=request)
            client.send(webpage)
            client.close()

