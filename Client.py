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
            data, addr = self.UDPClientSocket.recvfrom(1024)
            if(data is not None):
                print("Received: " + str(data))
                if(chr(data[0]) == "h"):
                    handShake = bytes("h", "utf-8") # or c for communication
                    prime = data[1:21]
                    prime = int.from_bytes(prime, byteorder='big')
                    generatorOfP = data[21 : 42]
                    generatorOfP = int.from_bytes(generatorOfP, byteorder='big')
                    ServerpublicKey = data[42 : 63]
                    ServerpublicKey = int.from_bytes(ServerpublicKey, byteorder='big')
                    self.secret = pow(ServerpublicKey, self.privateKey, prime)
                    print(self.secret)

    def listener(self):
        print("You called on the listener")

    def send(self, data):
        # Send to server using created UDP socket
        self.UDPClientSocket.sendto(bytes(data, "utf-8"), (self.localAdress, 5005))

    def handShake(self):
        handShake = bytes("h", "utf-8")
        self.privateKey = number.getRandomInteger(8*21)
        prime = number.getPrime(8 * 21)
        generatorOfP = number.getRandomInteger(8 * 21)
        publicKey = pow(generatorOfP, self.privateKey, prime)
        print("genOfP:" + str(generatorOfP))
        print("publicKey: " + str(publicKey))
        print("prime: " + str(prime))
        prime = prime.to_bytes(21, byteorder='big')
        generatorOfP = generatorOfP.to_bytes(21, byteorder='big')
        publicKey = publicKey.to_bytes(21, byteorder='big')
        data = handShake + prime + generatorOfP  + publicKey
        data += b"0" * (64 - len(data))
        self.UDPClientSocket.sendto( data , (self.localAdress, 5005))
        return

    def sendThroughSecProtocol(self, data):
        # Send to server using created UDP socket
        handShake()       
if __name__ == "__main__":
    client = Client(UDP_IP, UDP_PORT)
    #client.sendThroughSecProtocol("Hello webmaster Carl! How is it going with the server?")
    client.handShake()
    client.run()