import socket
from Crypto.Cipher import AES

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello World!"

class Server:
    #Constructor, we need to add self variable in constructor and methods in order to point to the object. 
    def __init__(self, localAdress, port):
        self.localAdress = localAdress
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

    def run(self):
        print("Welcome to server side!")
        print("Instance is running on: " + str(self.localAdress) + ":" + str(self.port))
        while(True):
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            if data is not None:
                print ("received message:", data)
                obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
                print ("decrypted data: ", obj2.decrypt(data))


    def listener(self):
        print("You called on the listener")
        
       

    def sender(self):
        print("You called on the sender")
        self.sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        
if __name__ == "__main__":    
    server = Server(UDP_IP, UDP_PORT)
    server.run()