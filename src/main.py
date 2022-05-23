import server_class
import sys

## bring up the a server
def server(port_):
    srv = server_class.Server(port=port_)
    srv.start()

## main
if __name__ == "__main__":
    port = int(sys.argv[1])
    server(port)
