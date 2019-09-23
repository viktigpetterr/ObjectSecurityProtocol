import socket
from Crypto.Cipher import AES
from Crypto.Util import number

UDP_IP = "127.0.0.1"
UDP_PORT = 5004

class Client:
    #Constructor, we need to add self variable in constructor and methods in order to point to the object. 
    def __init__(self, localAdress, port):
        self.localAdress = localAdress
        self.port = port
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # self.UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDPClientSocket.bind((localAdress, port))

    def run(self):
        print("Welcome to client side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            data = self.UDPClientSocket.recvfrom(1024)
            if(data is not None):
                print("Received: " + str(data))

    def listener(self):
        print("You called on the listener")

    def send(self, data):
        # Send to server using created UDP socket
        self.UDPClientSocket.sendto(bytes(data, "utf-8"), (self.localAdress, 5005))

    def handShake(self):
        handShake = bytes("h", "utf-8") # or c for communication
        privateKey = number.getRandomInteger(8)
        prime = number.getPrime(8)
        generatorOfP = number.getRandomInteger(8)
        publicKey = (generatorOfP ** privateKey) % prime
        prime = bytes([prime])
        generatorOfP = bytes([generatorOfP])
        publicKey = bytes([publicKey])
        self.UDPClientSocket.sendto( prime + generatorOfP  + publicKey , (self.localAdress, 5005))
        return True

    def sendThroughSecProtocol(self, data):
        # Send to server using created UDP socket
        handShake()       
if __name__ == "__main__":
    client = Client(UDP_IP, UDP_PORT)
    #client.sendThroughSecProtocol("Hello webmaster Carl! How is it going with the server?")
    client.handShake()