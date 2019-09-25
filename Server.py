import socket
from Crypto.Cipher import AES
from Crypto.Util import number

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Server:
    #Constructor, we need to add self variable in constructor and methods in order to point to the object. 
    def __init__(self, localAdress, port):
        self.localAdress = localAdress
        self.port = port
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind((localAdress, port))

    def run(self):
        print("Welcome to server side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            data, addr = self.UDPClientSocket.recvfrom(1024) # buffer size is 1024 bytes
            if(data is not None):
                if(chr(data[0]) == "h"):
                    print ("Received handshake from", addr)
                    self.handleHandshake(data)
                if(chr(data[0]) == "c" and (self.secret is not None)):
                    print("Received data from", addr)
                    self.handleSecureIncommingData(data)
                #print ("decrypted data: ", obj2.decrypt(data))

    def handleHandshake(self, data):
        handShake = bytes("h", "utf-8") # or c for communication
        self.privateKey = number.getRandomInteger(224)
        prime = data[1:257]
        prime = int.from_bytes(prime, byteorder='big')
        generatorOfP = data[257 : 285]
        generatorOfP = int.from_bytes(generatorOfP, byteorder='big')
        ClientpublicKey = data[285 : 541]
        ClientpublicKey = int.from_bytes(ClientpublicKey, byteorder='big')

        secret = pow(ClientpublicKey, self.privateKey, prime)
        self.secret = str(secret)[0:32]
        newPublicKey = pow(generatorOfP, self.privateKey, prime)
        prime = prime.to_bytes(256, byteorder='big')
        generatorOfP = generatorOfP.to_bytes(28, byteorder='big')
        newPublicKey = newPublicKey.to_bytes(256, byteorder='big')

        data = handShake + prime + generatorOfP  + newPublicKey
        #first byte is header, the rest is keys. 
        self.UDPClientSocket.sendto( data , (self.localAdress, 5004))
        print("Secret:", self.secret)

    def handleSecureIncommingData(self, data):
        communicationFlag = data[0].to_bytes(1,byteorder="big")
        nonce = data [1:12]
        ciphertext = data [12:46]
        mac = data [46:62]
        messageLength = data [62:64]
        aesCipher = AES.new(bytes(self.secret,'utf-8'), AES.MODE_CCM, nonce)
        aesCipher.update(communicationFlag)
        #cipher = AES.new(self.secret, AES.MODE_EAX, nonce)s
        secretMessage = aesCipher.decrypt(ciphertext)
        secretMessageConcat = secretMessage[0:int.from_bytes(messageLength, byteorder = 'big')]
        try: 
            aesCipher.verify(mac)
            data = secretMessageConcat.decode("utf-8")
            print("Success! Secret message: ", data)
        except ValueError:
            print ("Error: Either Key is not correct or message the message is corrupted")
        
if __name__ == "__main__":    
    server = Server(UDP_IP, UDP_PORT)
    server.run()