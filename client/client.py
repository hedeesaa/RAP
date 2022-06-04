from socket import *
import sys

"""
It is a Test Client to send a UDP request
Because nc in Mac doesnt support UPD broadcast request
"""


sock = socket(AF_INET, SOCK_DGRAM,IPPROTO_UDP)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.settimeout(10)


server_address = ('255.255.255.255', int(sys.argv[1]))
message = sys.argv[2]

try:
	
	# Send data
	print('sending: ' + message)
	sent = sock.sendto(message.encode("UTF-8"), server_address)

	# Receive response
	print('waiting to receive')
	
	while True:
		data, server = sock.recvfrom(4096)
		data = data.decode("UTF-8")
		print(data)
		if "Not-Valid" in data:
			break
	
except:
	print("Closing")
	sock.close()
finally:	
	sock.close()


