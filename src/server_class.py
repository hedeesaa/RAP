import socket
import threading
import client_class

class Server:
    """
    1- Creates a TCP Socket on a Specific port
    2- Start the TCP Socket on a thread
    3- Able to stop the TCP Socket and Thread
    """
    def __init__(self,port=6231,ip=socket.gethostbyname_ex(socket.gethostname())[-1][-1]):
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = []

    def listening(self):
        try:
            print(f"Server is Listening on {self.addr[0]}:{self.addr[1]} ...")
            self.socket.bind(self.addr)
            self.socket.listen()
            while True:
                conn, addr = self.socket.accept()
                client = client_class.Client(conn, addr)
                self.clients.append(client)
                client.start()
        except Exception as e:
            print(e)
            print(f"Closing Socket on {self.addr[0]}:{self.addr[1]}...")

    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

    def stop(self):
        print("Server is Going Down...")
        for client in self.clients:
            if client.is_alive() == True:
                client.stop()
        self.socket.close()
        self.server_thread.join()
