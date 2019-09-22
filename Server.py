import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Server:
    #Constructor, we need to add self variable in constructor and methods in order to point to the object. 
    def __init__(self, localAdress, port):
        self.localAdress = localAdress
        self.port = port

    def run():
        print("Welcome to client side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            pass

    def listener(self):
        print("You called on the listener")
        
    def sender(self):
        print("You called on the sender")

server = Server(UDP_IP, UDP_PORT)
server.run()