import server_class
import sys
from pynput import keyboard
from rap_controller import RAP
import peer_discovery
import coloredlogs, logging
##


## Bring Up the Server
def server(server_port_,peer_port_,server_name_):
    coloredlogs.install()
    rap = RAP()

    keyboard_listener = keyboard.Listener(on_press=stopping_program)
    keyboard_listener.start()

    peerDC = peer_discovery.PeerDC(port=peer_port_)
    peerDC.set_server(server_name_,server_port_)
    peerDC.start()
    
    srv = server_class.Server(port=server_port_,server_name=server_name_,keyboard_listener=keyboard_listener)
    srv.set_client_action(rap.controller)
    srv.start()
    logging.info("For Stopping the Program Enter <<ESC>>")
    keyboard_listener.join()
    rap.sstop()
    srv.stop()
    peerDC.stop()


## ESC Keyboard
def stopping_program(key):
    if key == keyboard.Key.esc :
        logging.error("ESC was Pressed")
        return False

## main
if __name__ == "__main__":
    if len(sys.argv) == 4:
        server_port = int(sys.argv[1])
        peer_port = int(sys.argv[2])
        server_name = (sys.argv[3])
        server(server_port,peer_port,server_name)
    else:
        print("Error, Add Arguments: python3 main.py [server_port] [broadcast_port] [server_name]")
        
