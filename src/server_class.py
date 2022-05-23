import socket
import threading

class Server:
    def __init__(self,port=6231,ip=socket.gethostbyname_ex(socket.gethostname())[-1][-1]):
        self.addr = (ip, port)
        self.buffer_size = 1024
        self.encoding_format = 'utf-8'
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def listening(self):
        try:
            self.socket.bind(self.addr)
            self.socket.listen()
            while True:
                conn, addr = self.socket.accept()
                print(conn, addr)
        except:
            print("Closing Socket")

    def start(self):
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

    def stop(self):
        self.socket.close()
        self.server_thread.join()