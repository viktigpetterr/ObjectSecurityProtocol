import socket
from Crypto.Cipher import AES
from Crypto.Util import number

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello World!"

class Server:
    #Constructor, we need to add self variable in constructor and methods in order to point to the object. 
    def __init__(self, localAdress, port):
        self.localAdress = localAdress
        self.port = port
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind((localAdress, port))

    def checkMessageType(self, data):
        if(str(chr(data[0]))=="h"):
            return "handShake"

    def run(self):
        print("Welcome to server side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            data, addr = self.UDPClientSocket.recvfrom(1024) # buffer size is 1024 bytes
            if data is not None:
                print ("received message:", data)
                if(chr(data[0]) == "h"):
                    handShake = bytes("h01", "utf-8") # or c for communication
                    self.privateKey = number.getRandomInteger(80)
                    prime = data[3:24]
                    prime = int.from_bytes(prime, byteorder='big')
                    generatorOfP = data[24 : 43]
                    generatorOfP = int.from_bytes(generatorOfP, byteorder='big')
                    ClientpublicKey = data[43 : 64]
                    ClientpublicKey = int.from_bytes(ClientpublicKey, byteorder='big')
                    self.secret = pow(ClientpublicKey, self.privateKey, prime)
                    newPublicKey = pow(generatorOfP, self.privateKey, prime)
                    prime = prime.to_bytes(21, byteorder='big')
                    newPublicKey = newPublicKey.to_bytes(21, byteorder='big')
                    generatorOfP = generatorOfP.to_bytes(21, byteorder='big')
                    data = handShake + prime + generatorOfP  + newPublicKey
                    data += b"0" * (64 - len(data))
                    self.UDPClientSocket.sendto( data , (self.localAdress, 5004))
                    print(self.secret)
                obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
                #print ("decrypted data: ", obj2.decrypt(data))

    def listener(self):
        print("You called on the listener")

    def sender(self):
        print("You called on the sender")
        self.UDPClientSocket.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        UDPClientSocket.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        
if __name__ == "__main__":    
    server = Server(UDP_IP, UDP_PORT)
    server.run()