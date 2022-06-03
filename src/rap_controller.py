import rap_model
import socket
import json
import threading
import time
import logging
##

class RAP:
    ERROR_VARIABLE_NOT_EXIST = "This Variable is not existed!"
    def __init__(self):
        self.repo = {}
        self.peers= []
        self.go = True
        self.search =  threading.Thread(target=self.look_for_handler)
        self.search.start()

    def controller(self, msg):
        if self.__check_input(msg):
            command = msg.split()
            if command[0].upper() == "SET":
                if len(command) == 3:
                    output = command[1].split(".")
                    if len(output) == 2:
                        new_command = command[0]+" "+output[1]+" "+command[-1]
                        error, res = self.send_package_to_peer(output[0],new_command)
                        return res
                    else:
                        error, self.repo=rap_model.set_variable(command[1], int(command[2]),self.repo)
                        if error == False:
                            return "OK"
                return "[Error]: SET variable value"

            if command[0].upper() == "ADD":
                if len(command) == 3:
                    output = command[1].split(".")
                    if len(output) == 2:
                        new_command = command[0]+" "+output[1]+" "+command[-1]
                        error, res = self.send_package_to_peer(output[0],new_command)
                        return  res
                    else:
                        error, self.repo=rap_model.add_to_variable(command[1], int(command[2]),self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return "OK"
                return "[Error]: ADD variable value"

            if command[0].upper() == "DELETE":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        new_command = command[0]+" "+output[1]
                        error, res = self.send_package_to_peer(output[0],new_command)
                        return  res
                    else:
                        error, self.repo=rap_model.delete_variable(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return "OK"
                return "[Error]: DELETE variable"
                

            if command[0].upper() == "LIST":
                if len(command) == 2:
                    new_command = command[0]
                    error, res = self.send_package_to_peer(command[1],new_command)
                    return  res
                else:
                    error, keys=rap_model.list_keys(self.repo)
                    if error == False:
                        return keys

            if command[0].upper() == "GET":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        new_command = command[0]+" "+output[1]
                        error, res = self.send_package_to_peer(output[0],new_command)
                        return res
                    else:
                        error, value = rap_model.get_value(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return str(value)
                return "[Error]: GET variable"

            if command[0].upper() == "GET_VALUES":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        new_command = command[0]+" "+output[1]
                        error, res = self.send_package_to_peer(output[0],new_command)
                        return res
                    else:
                        error, value = rap_model.get_values(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return str(value)
                return "[Error]: GET_VALUES variable"
                
            if command[0].upper() == "SUM":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        new_command = command[0]+" "+output[1]
                        error, res = self.send_package_to_peer(output[0],new_command)
                        return res
                    else:
                        error, value = rap_model.sum_of_variable(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return value
                return "[Error]: SUM variable"

            if command[0].upper() == "RESET":
                if len(command) == 2:
                    new_command = command[0]
                    error, res = self.send_package_to_peer(command[1],new_command)
                    return res
                else:
                    error, self.repo = rap_model.reset()
                    return "OK"
            
            if command[0].upper() == "FINISH":
                return "FIN"
            
            if command[0].upper() == "DSUM":
                command[2] = "including".upper()
                peers = command[command.index('INCLUDING')+1:]

                sums = []
                for peer in peers:
                    new_command = "sum "+command[1]
                    error, res = self.send_package_to_peer(peer,new_command)
                    if error == None:
                        res = res.strip()
                        sums.append(int(res))
                    else:
                        return res
                return sum(sums)
                
                
        return "[COMMAND IS NOT ACCEPTABLE] Eligible commands are FINISH, RESET, SUM, GET_VALUES, LIST, GET, DELETE, ADD, DSUM"

    def __check_input(self, msg):
        """
        Checks Message Input of a User
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0].upper()
            if command in ["FINISH", "RESET", "SUM","GET_VALUES" , "LIST" , "GET", "DELETE", "ADD", "SET","DSUM"]:
                return True
        return False

    def look_for_handler(self):
        while self.go:
            self.look_for_peers(6233)
            logging.info(self.peers)
            time.sleep(10)

    def look_for_peers(self,port):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(10)

        server_address = ('255.255.255.255', port)
        message = "serverList"

        try:
            
            # Send data
            sent = sock.sendto(message.encode("UTF-8"), server_address)

            # Receive response
            while True:
                data, server = sock.recvfrom(4096)
                data = data.decode("UTF-8")
                data = json.loads(data)
                if data not in self.peers:
                    self.peers.append(data)
        except:
            sock.close()
        finally:	
            sock.close()


    def look_if_peer_exists(self,peer_name_):
        for peer in self.peers:
            if peer["ServerName"] == peer_name_:
                return None, peer
        
        return "Error", None
    

    def send_package_to_peer(self,peer_name,command):
        error, peer=self.look_if_peer_exists(peer_name)
        if error == None:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer["IP"], peer["Port"]))
            res = sock.recv(1024)
            sock.send(command.encode('utf-8'))
            res = sock.recv(1024).decode('utf-8')
            sock.close()
            if res.strip() == RAP.ERROR_VARIABLE_NOT_EXIST:
                return "Error", RAP.ERROR_VARIABLE_NOT_EXIST

            return None, res
        
        return "Error", f"Peer {peer} Does Not Exist"

    def sstop(self):
        self.go = False
        