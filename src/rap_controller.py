import rap_model
import socket
import json
class RAP:
    def __init__(self, id):
        self.id = id
        self.repo = {}
        self.res = {}
    def controller(self, msg):
        
        if self.__check_input(msg):
            command = msg.split()
            
            if command[0].upper() == "SET":
                output = command[1].split(".")
                if len(output) == 2:
                    self.look_for_peers(output[0],6233)
                    if self.res:
                        if self.res["Error"] == "None":
                            new_command = command[0]+" "+output[1]+" "+command[-1]
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                            sock.connect(("192.168.2.18", 6234))
                            res = sock.recv(1024)
                            sock.send(new_command.encode('utf-8'))
                            res = sock.recv(1024).decode('utf-8')
                            sock.close()
                            return res
                        else:
                            return "Not-Valid"    
                    else:
                        print("The peer doesnt exists")
                        return "False"
                else:
                    self.repo=rap_model.set_variable(command[1], int(command[2]),self.repo)
                return "OK"

            if command[0].upper() == "ADD":
                self.repo, error=rap_model.add_to_variable(command[1], int(command[2]),self.repo)
                if error:
                    return "This Variable is not existed!"
                return "OK"

            if command[0].upper() == "DELETE":
                self.repo, error=rap_model.delete_variable(command[1],self.repo)
                if error:
                    return "This variable doesnt exist!"
                return "OK"
                

            if command[0].upper() == "LIST":
                keys=rap_model.list_keys(self.repo)
                return keys

            if command[0].upper() == "GET":
                value, error = rap_model.get_value(command[1],self.repo)
                if error:
                    return "This variable doesnt exist!"
                return str(value)

            if command[0].upper() == "GET_VALUES":
                value, error = rap_model.get_values(command[1],self.repo)
                if error:
                    return "This variable doesnt exist!"
                return str(value)
                
            if command[0].upper() == "SUM":
                value, error = rap_model.sum_of_variable(command[1],self.repo)
                if error:
                    return "This variable doesnt exist!"
                return value

            if command[0].upper() == "RESET":
                self.repo = rap_model.reset()
                return "OK"
            
            if command[0].upper() == "FINISH":
                return "FIN"
            
        return "[COMMAND IS NOT ACCEPTABLE] Eligible commands are FINISH, RESET, SUM, GET_VALUES, LIST, GET, DELETE, ADD"

    def __check_input(self, msg):
        """
        checks message input of user
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0].upper()
            if command in ["FINISH", "RESET", "SUM","GET_VALUES" , "LIST" , "GET", "DELETE", "ADD", "SET"]:
                return True
            else:
                return False
        else:
            return False

    def look_for_peers(self,lserver,port):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(10)


        server_address = ('255.255.255.255', port)
        message = "serverList"

        try:
            
            # Send data
            print('sending: ' + message)
            sent = sock.sendto(message.encode("UTF-8"), server_address)

            # Receive response
            print('waiting to receive')
            
            while True:
                data, server = sock.recvfrom(4096)
                data = data.decode("UTF-8")
                data = json.loads(data)
                if data["ServerName"] ==  lserver:
                    self.res = data
                    break
        except:
            print("Closing")
            sock.close()
        finally:	
            sock.close()

    
        