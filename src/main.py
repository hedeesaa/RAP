import server_class
import sys
import time
from pynput import keyboard

## bring up the a server
def server(port_):
    srv = server_class.Server(port=port_)
    srv.start()
    print("For Stopping program enter <<ESC>>")
    keyboard_listener = keyboard.Listener(on_press=stopping_program,arg=srv)
    keyboard_listener.start()
    keyboard_listener.join()
    srv.stop()

def stopping_program(key):
    if key == keyboard.Key.esc:
        print("ESC was pressed")
        return False

## main
if __name__ == "__main__":
    port = int(sys.argv[1])
    server(port)
    
