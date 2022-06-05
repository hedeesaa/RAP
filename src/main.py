import server_class
import sys
from pynput import keyboard
from rap_controller import RAP
from peer_discovery import ERAP
import coloredlogs, logging
import time
##

## Bring Up the Server
def server(server_port_,server_name_,peer_port_):
    coloredlogs.install()
    
    if peer_port_ != None:
            erap = ERAP(server_name_,server_port_,port=peer_port_)
            erap.start()
            rap = RAP(erap)
    else:
        rap = RAP()
    
    srv = server_class.Server(port=server_port_,server_name=server_name_)
    srv.set_client_action(rap.controller)
    srv.start()

    time.sleep(3)

    if srv.is_alive():
        keyboard_listener = keyboard.Listener(on_press=stopping_program)
        keyboard_listener.start()
        
        logging.info("For Stopping the Program Enter <<ESC>>")
        ## Waits for Until keyboard stops the program
        keyboard_listener.join()
        srv.stop()

    if peer_port_ != None:
        erap.stop()

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
        
