import socket
import threading
import json
import logging

class ERAP:

    ESOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    ESOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    ESOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    BUFFERSIZE  = 1024
    ENCODING_METHOD = "UTF-8"

    def __init__(self,server_name, server_port,port=6231):
        self.eport = port
        self.addr = ('0.0.0.0', self.eport)
        self.srv_name = server_name
        self.srv_host = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
        self.srv_port = server_port

        self.peers = []

    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()
        
    def listening(self):
        try:
            logging.info(f"UDP Server is Up and Listening {self.addr[0]}:{self.addr[1]} ...")
            ERAP.ESOCKET.bind(self.addr)
            while True:
                ## Waiting for user
                ## Blocking
                message, address = ERAP.ESOCKET.recvfrom(ERAP.BUFFERSIZE)
                message = message.decode(ERAP.ENCODING_METHOD)

                if message == "serverList":
                    msgFromServer = {
                        "ServerName": f"{self.srv_name}",
                        "IP": f"{self.srv_host}",
                        "Port": self.srv_port,
                        "Error": "None"
                        }
                else:
                    msgFromServer = {
                        "Error": "Not-Valid: To receive list of servers type <<serverList>>"
                    }
                msgFromServer = json.dumps(msgFromServer)

                logging.info(f"BroadCast Reseponse: {msgFromServer}")
                ERAP.ESOCKET.sendto(msgFromServer.encode(ERAP.ENCODING_METHOD), address)  

        except:
            logging.error(f"Closing UDP Server...")
            ERAP.ESOCKET.close()
            
    def stop(self):
        ERAP.ESOCKET.close()

    def look_for_peers(self):
        self.psocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.psocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.psocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.psocket.settimeout(10)

        server_address = ('255.255.255.255', self.eport)
        message = "serverList"

        try:
            # Send data
            self.psocket.sendto(message.encode(ERAP.ENCODING_METHOD), server_address)
            # Receive response
            while True:
                data, _ = self.psocket.recvfrom(ERAP.BUFFERSIZE)
                data = data.decode(ERAP.ENCODING_METHOD)
                data = json.loads(data)
                if data not in self.peers:
                    self.peers.append(data)
        except:
            self.psocket.close()
        finally:
            logging.info(self.peers)

    def look_if_peer_exists(self,peer_name_):
        for peer in self.peers:
            if peer["ServerName"] == peer_name_:
                return None, peer
        return "Error", None

    def send_package_to_peer(self,peer_name,command):

        error, peer=self.look_if_peer_exists(peer_name)

        if error == None:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer["IP"], peer["Port"]))
            res = sock.recv(ERAP.BUFFERSIZE)
            sock.send(command.encode(ERAP.ENCODING_METHOD))
            res = sock.recv(ERAP.BUFFERSIZE).decode(ERAP.ENCODING_METHOD)
            sock.close()

            if res.strip() == "This Variable is not existed!":
                return "Error", "This Variable is not existed!"
            return None, res

        return "Error", f"Peer {peer} Does Not Exist"

    