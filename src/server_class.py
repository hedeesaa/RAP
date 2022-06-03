import socket
import threading
import client_class
from rap_controller import RAP
import logging

class Server:
    """
    1- Creates a TCP Socket on a Specific port
    2- Start the TCP Socket on a thread
    3- Able to stop the TCP Socket and Thread
    """
    def __init__(self,keyboard_listener,server_name, port=6231,ip=socket.gethostbyname_ex(socket.gethostname())[-1][-1]):
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = []
        self.client_action = lambda x : x
        self.server_name = server_name
        self.keyboard_listener = keyboard_listener
        

    def listening(self):
        try:
            logging.info(f"Server is Listening on {self.addr[0]}:{self.addr[1]} ...")
            self.socket.bind(self.addr)
            self.socket.listen()
            while True:
                conn, addr = self.socket.accept()
                client = client_class.Client(conn, addr)
                client.action(self.client_action)
                self.clients.append(client)
                client.start(self.server_name)
        except OSError:
            logging.info(f"Closing Socket on {self.addr[0]}:{self.addr[1]}...")
            self.stop_yourself()

    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

    def stop(self):
        logging.info("Server is Going Down...")
        for client in self.clients:
            if client.is_alive() == True:
                client.stop()
        self.socket.close()
        self.server_thread.join()
    
    def stop_yourself(self,):
        for client in self.clients:
            if client.is_alive() == True:
                client.stop()
        self.socket.close()
        self.keyboard_listener.stop()
        

    def set_client_action(self,func):
        self.client_action = func
    