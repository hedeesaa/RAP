import socket
import threading
from rap_controller import RAP


PORT = 6232
SERVER_IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
ADDR = (SERVER_IP, PORT)
BUFFER_SIZE = 1024
ENCODING_FORMAT = 'utf-8'
thread_list = []
ID = 1



## What type of IP address that we are going to accept, AF_INET is for IPV4
## Streaming data to the socket, There are different types of sending data to the socket
SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def client_handling(conn_, addr_):
    print(f"[NEW CONNECTION] {addr_} started!")
    ## Creating an RAP instance 
    conn_.send(f"OK Repository << {rap.id} >> Ready.\n".encode(ENCODING_FORMAT))
    ## The bufsize argument of 1024 used above is the maximum amount of data to be received at once.
    with conn_:
        while True:
            ## recving is blocking as well
            msg = (conn_.recv(BUFFER_SIZE).decode(ENCODING_FORMAT)).strip()
            respond = rap.controller(msg)
            if respond == "FIN":
                print(f"[{addr_}]: CONNECTION TERMINATED")
                break
            conn_.send(f"{respond}\n".encode(ENCODING_FORMAT))


def start_server():
    # A listening socket does just what its name suggests. It listens for connections from clients. When a client connects, the server calls .accept() to accept, or complete, the connection.
    SERVER.listen()
    print(f"Server is listening on {SERVER_IP}:{PORT}")
    print("To stop the server, press ESC")
    while True:
        ## it is waiting for a new connection to the server. and program will be blocked here
        ## conn is to return data back and addr is for storing clients port and IP
        conn, addr = SERVER.accept()
        client = threading.Thread(target=client_handling, args=(conn,addr))
        thread_list.append(client)
        client.start()
        
    
# TODO STOP SERVER
def stop_server(key):
    pass

    




## Now it's time to bind our socket to a address
SERVER.bind(ADDR)
rap = RAP(1)
main_thread = threading.Thread(target=start_server)
main_thread.start()