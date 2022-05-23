import threading

class Client:

    def __init__(self, conn, addr, buffer_size=1024,encoding_format='utf-8' ):
        self.conn = conn
        self.addr = addr
        self.encoding_format = encoding_format
        self.buffer_size = buffer_size
        self.alive = True


    def handler(self):
        print(f"[NEW CONNECTION] {self.addr[0]}:{self.addr[1]} started!")
        ## Creating an RAP instance 
        ## The bufsize argument of 1024 used above is the maximum amount of data to be received at once.
        with self.conn:
            try:
                while True:
                ## recving is blocking as well
                    msg = (self.conn.recv(self.buffer_size).decode(self.encoding_format)).strip()
                    if not msg: 
                        print(f"[Terminated] Client {self.addr[0]}:{self.addr[1]} Terminated its Connection!")
                        self.alive = False
                        break
                    print(msg)
                    respond = "hello"
                    self.conn.send(f"{respond}\n".encode(self.encoding_format))
            except:
                print(f"Connection {self.addr[0]}:{self.addr[1]} is closed")

    def start(self):
        self.client_thread = threading.Thread(target=self.handler)
        self.client_thread.start()

    def stop(self):
        self.conn.send(f"Server is Closing the Connection\n".encode(self.encoding_format))
        self.conn.close()
    
    def is_alive(self):
        return self.alive

