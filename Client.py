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
        self.UDPClientSocket.bind((localAdress, port))

    def run(self):
        print("Welcome to client side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            message = input("Message to server (max 34 characters): ")
            dataHasBeenSent = False
            client.handShake()
            while(dataHasBeenSent is not True):
                data, addr = self.UDPClientSocket.recvfrom(1024)
                if(data is not None):
                    if(chr(data[0]) == "h"):
                        print("Handshake retrived from:", addr)
                        handShake = bytes("h", "utf-8") # or c for communication
                        prime = data[1:257]
                        prime = int.from_bytes(prime, byteorder='big')
                        generatorOfP = data[257 : 285]
                        generatorOfP = int.from_bytes(generatorOfP, byteorder='big')
                        serverPublicKey = data[285 : 541]
                        serverPublicKey = int.from_bytes(serverPublicKey, byteorder='big')
                        secret = pow(serverPublicKey, self.privateKey, prime)
                        self.secret = str(secret)[0:32]
                        print("Secret:", self.secret)
                        #Time to send data securily.
                        self.sendEncryptedData(message)
                        print("Data sent to server")
                        dataHasBeenSent = True
                    if(chr(data[0] == "c") and (self.secret is not None)):
                        print("Data retrived from:", addr)

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
        print("Sent Handshake to establish secure connection")

    def sendEncryptedData(self, message):
        communicationFlag = bytes("c", "utf-8")
        aesCipher = AES.new(bytes(self.secret,'utf-8'), AES.MODE_CCM)
        nonce = aesCipher.nonce
        messageLength = len(message).to_bytes(2, byteorder="big")
        by = bytes(message, "utf-8")
        by += b"0" * (34 - len(by))
        aesCipher.update(communicationFlag)
        encryption = aesCipher.encrypt(by)
        mac = aesCipher.digest()
        data = communicationFlag + nonce  + encryption + mac + messageLength
        self.UDPClientSocket.sendto(data , (self.localAdress, 5005))

if(__name__ == "__main__"):
    client = Client(UDP_IP, UDP_PORT)
    client.run()