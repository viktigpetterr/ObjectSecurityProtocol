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
                print("Received data!")
                if(chr(data[0]) == "h"):
                    handShake = bytes("h", "utf-8") # or c for communication
                    prime = data[1:257]
                    prime = int.from_bytes(prime, byteorder='big')
                    generatorOfP = data[257 : 285]
                    generatorOfP = int.from_bytes(generatorOfP, byteorder='big')
                    serverPublicKey = data[285 : 541]
                    serverPublicKey = int.from_bytes(serverPublicKey, byteorder='big')
                    self.secret = pow(serverPublicKey, self.privateKey, prime)
                    print("Secret:", self.secret)

    def send(self, data):
        # Send to server using created UDP socket
        self.UDPClientSocket.sendto(bytes(data, "utf-8"), (self.localAdress, 5005))

    def handShake(self):
        handShake = bytes("h", "utf-8")

        self.privateKey = number.getRandomNBitInteger(224)
        prime = number.getPrime(2048)
        generatorOfP = number.getRandomNBitInteger(224)
        publicKey = pow(generatorOfP, self.privateKey, prime)

        prime = prime.to_bytes(256, byteorder='big') # From int to byteString
        generatorOfP = generatorOfP.to_bytes(28, byteorder='big')
        publicKey = publicKey.to_bytes(256, byteorder='big')

        data = handShake + prime + generatorOfP  + publicKey # 1 + 256 + 28 + 256 bytes
        
        self.UDPClientSocket.sendto( data , (self.localAdress, 5005))
      
if __name__ == "__main__":
    client = Client(UDP_IP, UDP_PORT)
    #client.sendThroughSecProtocol("Hello webmaster Carl! How is it going with the server?")
    client.handShake()
    client.run()