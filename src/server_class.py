import socket
import threading
import client_class
import logging

class Server:
    """
    1- Creates a TCP Socket on a Specific port
    2- Start the TCP Socket on a thread
    3- Able to stop the TCP Socket and Thread
    4- To stop clients of server it must receive FIN
    """
    def __init__(self,server_name, port=6231,ip=socket.gethostbyname_ex(socket.gethostname())[-1][-1]):
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.client_action = lambda x : x
        self.server_name = server_name
        self.alive = False

    def listening(self):
        try:
            logging.info(f"Server is Listening on {self.addr[0]}:{self.addr[1]} ...")
            self.socket.bind(self.addr)
            self.socket.listen()
            self.alive = True
            while True:
                conn, addr = self.socket.accept()
                client = client_class.Client(conn, addr)
                client.action(self.client_action)
                self.clients.append(client)
                client.start(self.server_name)
        except Exception as e:
            a = str(e)
            if "Address already in use" in a:
                logging.error("Address is Already in Use")
                self.stop_yourself()
            logging.error(f"Connection of Server [{self.addr[0]}:{self.addr[1]}] is Closed ...")
            
    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

    def stop(self):
        self.stop_yourself()
        self.server_thread.join()
    
    def stop_yourself(self):
        logging.error("Server is Going Down...")
        for index,client in enumerate(self.clients): 
            try:
                if client.is_alive() == True:
                    client.stop()
                    logging.error(f"Client Connection {index} has Closed!")
            except:
                continue
        self.socket.close()
        
    def set_client_action(self,func):
        self.client_action = func

    def is_alive(self):
        return self.alive
    