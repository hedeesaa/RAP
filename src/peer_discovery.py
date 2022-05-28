import socket
import threading

class PeerDC:
## TODO Make peer discovery, it just reponse the client
## TODO Make peers find each other for proxy

    def __init__(self, server_name, port=6231):
        self.addr = ('', port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.client_action = lambda x : x
        self.server_name = server_name
        self.bufferSize  = 1024

    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

## TODO make better response
    def listening(self):
        try:
            print(f"UDP server up and listening {self.addr[0]}:{self.addr[1]} ...")
            self.socket.bind(self.addr)
            while True:
                bytesAddressPair = self.socket.recvfrom(self.bufferSize)
                
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]

                clientMsg = "Message from Client:{}".format(message)
                clientIP  = "Client IP Address:{}".format(address)
    
                print(clientMsg)
                print(clientIP)

                ip=socket.gethostbyname_ex(socket.gethostname())[-1][-1]
                msgFromServer= f"I am from {ip}:{self.addr[1]}"

                bytesToSend= str.encode(msgFromServer)

                self.socket.sendto(bytesToSend, address)

        except OSError:
            print(f"Closing UDP")

## TODO make better stop            
    def stop(self):
        self.socket.close()