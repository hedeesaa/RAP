import server_class
import sys
from pynput import keyboard
from rap_controller import RAP
import peer_discovery


## bring up the a server
def server(port_,server_name_):
    rap = RAP(server_name_)
    keyboard_listener = keyboard.Listener(on_press=stopping_program)
    keyboard_listener.start()

    peerDC = peer_discovery.PeerDC(port=port_,server_name=server_name_)
    peerDC.start()
    
    srv = server_class.Server(port=port_,server_name=server_name_,keyboard_listener=keyboard_listener)
    srv.set_client_action(rap.controller)
    srv.start()
    print("For Stopping program enter <<ESC>>")
    keyboard_listener.join()
    srv.stop()
    peerDC.stop()


def stopping_program(key):
    if key == keyboard.Key.esc :
        print("ESC was pressed")
        return False

## main
if __name__ == "__main__":
    port = int(sys.argv[1])
    server_name = (sys.argv[2])
    server(port,server_name)
    
