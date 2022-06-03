import threading
import logging

class Client:

    def __init__(self, conn, addr, buffer_size=1024,encoding_format='utf-8' ):
        self.conn = conn
        self.addr = addr
        self.encoding_format = encoding_format
        self.buffer_size = buffer_size
        self.alive = True
        self.action_function = lambda x: x


    def handler(self):
        logging.info(f"[NEW CONNECTION] {self.addr[0]}:{self.addr[1]} started!")
        self.greeting(f"Repository << {self.parent_name} >> Ready.")
        ## Creating an RAP instance 
        ## The bufsize argument of 1024 used above is the maximum amount of data to be received at once.
        with self.conn:
            try:
                while True:
                ## recving is blocking as well
                    msg = (self.conn.recv(self.buffer_size).decode(self.encoding_format)).strip()
                    if not msg: 
                        logging.info(f"[Terminated] Client {self.addr[0]}:{self.addr[1]} Terminated its Connection!")
                        self.alive = False
                        break
                    logging.info(msg)
                    respond = self.action_function(msg)
                    if respond == "FIN":
                        self.conn.close()
                        break
                    else:
                        self.conn.send(f"{respond}\n".encode(self.encoding_format))
            except Exception as e:
                logging.info(f"Connection {self.addr[0]}:{self.addr[1]} is closed")

    def start(self,server_name):
        self.parent_name = server_name
        self.client_thread = threading.Thread(target=self.handler)
        self.client_thread.start()

    def stop(self):
        self.conn.send(f"Server is Closing the Connection\n".encode(self.encoding_format))
        self.conn.close()
    
    def is_alive(self):
        return self.alive

    def action(self, action_function):
        self.action_function = action_function

    def greeting(self,string):
        self.conn.send(f"{string}\n".encode(self.encoding_format))

   
