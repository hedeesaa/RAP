import server_class
import sys
from pynput import keyboard
from rap_controller import RAP
import peer_discovery
import coloredlogs, logging
##


## Bring Up the Server
def server(server_port_,server_name_,peer_port_):
    coloredlogs.install()
    

    keyboard_listener = keyboard.Listener(on_press=stopping_program)
    keyboard_listener.start()

    if peer_port_ != None:
        peerDC = peer_discovery.PeerDC(port=peer_port_)
        peerDC.set_server(server_name_,server_port_)
        peerDC.start()
        rap = RAP(peerDC)
    else:
        rap = RAP(None)
    
    srv = server_class.Server(port=server_port_,server_name=server_name_,keyboard_listener=keyboard_listener)
    srv.set_client_action(rap.controller)
    srv.start()
    logging.info("For Stopping the Program Enter <<ESC>>")
    keyboard_listener.join()
    rap.sstop()
    srv.stop()
    if peer_port_ != None:
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
        server(server_port,server_name,peer_port)
    elif len(sys.argv) == 3:
        server_port = int(sys.argv[1])
        server_name = (sys.argv[2])
        server(server_port,server_name,None)
    else:
        print("Error, Add Arguments: python3 main.py [server_port] [broadcast_port] [server_name]")
        
