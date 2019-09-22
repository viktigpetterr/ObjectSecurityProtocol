import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Client:
    #Constructor
    def __init__(localAdress, port):
        self.localAdress = localAdress
        self.port = port
    def run(self):
        print("Welcome to server side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            pass
    def listener(self):
        print("You called on the listener")
    def sender(self):
        print("You called on the sender")

client = Client(UDP_IP, UDP_PORT )
client.run()