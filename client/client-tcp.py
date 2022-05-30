import socket

port = 6231
host  = "192.168.2.18"
print(host,port )
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect((host, port))
command = "set a 2"
sock.send(command.encode('utf-8'))
res = sock.recv(1024)
print(res)
sock.close()