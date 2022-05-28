from socket import *

# Create a UDP socket
sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.settimeout(5)

server_address = ('255.255.255.255', 6231)
message = 'hey'

try:
	while True:
		# Send data
		print('sending: ' + message)
		sent = sock.sendto(message.encode(), server_address)

		# Receive response
		print('waiting to receive')
		data, server = sock.recvfrom(4096)
		data = data.decode('UTF-8')
		if "I am from" in data:
			print('Received confirmation')
			print(data)
			print('Server ip: ' + str(server[0]) )
			print('Server port: ' + str(server[1]) )
			break
		else:
			print('Verification failed')
		
		print('Trying again...')
	
	
finally:	
	sock.close()
