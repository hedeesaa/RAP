import socket
import threading
import json
import logging

class PeerDC:

    def __init__(self, port=6231):
        self.addr = ('0.0.0.0', port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_action = lambda x : x
        self.bufferSize  = 1024

    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

    def set_server(self,server_name,srv_port):
        self.server_name = server_name
        self.srv_host = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
        self.srv_port = srv_port
        
    def listening(self):
        try:
            logging.info(f"UDP server up and listening {self.addr[0]}:{self.addr[1]} ...")
            self.socket.bind(self.addr)
            while True:
                bytesAddressPair = self.socket.recvfrom(self.bufferSize)
                

                message = bytesAddressPair[0].decode("UTF-8")
                address = bytesAddressPair[1]


                if message == "serverList":
                    msgFromServer = {
                        "ServerName": f"{self.server_name}",
                        "IP": f"{self.srv_host}",
                        "Port": self.srv_port,
                        "Error": "None"
                        }
                    
                else:
                    msgFromServer = {
                        "Error": "Not-Valid: To receive list of servers type <<serverList>>"
                    }
                logging.info(msgFromServer)
                msgFromServer = json.dumps(msgFromServer)

                logging.info(f"Broadcast Reseponse: {msgFromServer}")  
                bytesToSend= str.encode(msgFromServer)
                self.socket.sendto(bytesToSend, address)  

        except OSError:
            logging.error(f"Closing UDP Server...")
          
    def stop(self):
        self.socket.close()