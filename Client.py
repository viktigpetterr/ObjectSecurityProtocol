import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Client:
    #Constructor, we need to add self variable in constructor and methods in order to point to the object. 
    def __init__(self, localAdress, port):
        self.localAdress = localAdress
        self.port = port
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def run(self):
        print("Welcome to client side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            data = self.UDPClientSocket.recvfrom(1024)
            if(data not null):
                print("Received: " + str(data))

    def listener(self):
        print("You called on the listener")

    def send(self, data):
        # Send to server using created UDP socket
        self.UDPClientSocket.sendto(data, 5005)
        print("You called on the sender")

if __name__ == "__main__":
    client = Client(UDP_IP, UDP_PORT)
    #client.run()
    clinet.send("Hello webmaster Carl! How is it going with the server?")