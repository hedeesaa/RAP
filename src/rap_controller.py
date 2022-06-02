import rap_model
import socket
import json
import threading
import time
class RAP:
    def __init__(self, id):
        self.id = id
        self.repo = {}
        self.peers= []
        self.go = True
        self.search =  threading.Thread(target=self.look_for_handler)
        self.search.start()
    def controller(self, msg):
        
        if self.__check_input(msg):
            command = msg.split()
            if command[0].upper() == "SET":
                output = command[1].split(".")
                if len(output) == 2:
                    new_command = command[0]+" "+output[1]+" "+command[-1]
                    res, error = self.send_package_to_peer(output[0],new_command)
                    return res
                else:
                    self.repo=rap_model.set_variable(command[1], int(command[2]),self.repo)
                    return "OK"

            if command[0].upper() == "ADD":
                output = command[1].split(".")
                if len(output) == 2:
                    new_command = command[0]+" "+output[1]+" "+command[-1]
                    error, result=self.look_if_peer_exists(output[0])
                    res, error = self.send_package_to_peer(output[0],new_command)
                    return  res
                else:
                    self.repo, error=rap_model.add_to_variable(command[1], int(command[2]),self.repo)
                    if error:
                        return "This Variable is not existed!"
                    return "OK"

            if command[0].upper() == "DELETE":
                output = command[1].split(".")
                if len(output) == 2:
                    new_command = command[0]+" "+output[1]
                    error, result=self.look_if_peer_exists(output[0])
                    res, error = self.send_package_to_peer(output[0],new_command)
                    return  res
                else:
                    self.repo, error=rap_model.delete_variable(command[1],self.repo)
                    if error:
                        return "This variable doesnt exist!"
                    return "OK"
                

            if command[0].upper() == "LIST":
                if len(command) == 2:
                    new_command = command[0]
                    error, result=self.look_if_peer_exists(command[1])
                    res, error = self.send_package_to_peer(command[1],new_command)
                    return  res
                else:
                    keys=rap_model.list_keys(self.repo)
                    return keys

            if command[0].upper() == "GET":
                output = command[1].split(".")
                if len(output) == 2:
                    new_command = command[0]+" "+output[1]
                    error, result=self.look_if_peer_exists(output[0])
                    res, error = self.send_package_to_peer(output[0],new_command)
                    return res
                else:
                    value, error = rap_model.get_value(command[1],self.repo)
                    if error:
                        return "This variable doesnt exist!"
                    return str(value)

            if command[0].upper() == "GET_VALUES":
                output = command[1].split(".")
                if len(output) == 2:
                    new_command = command[0]+" "+output[1]
                    error, result=self.look_if_peer_exists(output[0])
                    res, error = self.send_package_to_peer(output[0],new_command)
                    return res
                else:
                    value, error = rap_model.get_values(command[1],self.repo)
                    if error:
                        return "This variable doesnt exist!"
                    return str(value)
                
            if command[0].upper() == "SUM":
                output = command[1].split(".")
                if len(output) == 2:
                    new_command = command[0]+" "+output[1]
                    error, result=self.look_if_peer_exists(output[0])
                    res, error = self.send_package_to_peer(output[0],new_command)
                    return res
                else:
                    value, error = rap_model.sum_of_variable(command[1],self.repo)
                    if error:
                        return "This variable doesnt exist!"
                    return value

            if command[0].upper() == "RESET":
                if len(command) == 2:
                    new_command = command[0]
                    error, result=self.look_if_peer_exists(command[1])
                    res, error = self.send_package_to_peer(command[1],new_command)
                    return res
                else:
                    self.repo = rap_model.reset()
                    return "OK"
            
            if command[0].upper() == "FINISH":
                return "FIN"
            
            if command[0].upper() == "DSUM":
                output = command[command.index('including')+1:]
                sums = []
                for i in output:
                    error, result=self.look_if_peer_exists(i)

                    if error == None:
                        print("I am in the error==none")
                        new_command = "sum "+command[1]
                        print(new_command)
                        res, error = self.send_package_to_peer(i,new_command)
                        a = int(error.strip())
                        print(a)
                        sums.append(a)
                    else:
                        return f"Peer {i} doesnt exist"
                
                return sum(sums)
                

                # if len(output) == 2:
                #     new_command = command[0]+" "+output[1]
                #     error, result=self.look_if_peer_exists(output[0])
                #     return self.send_package_to_peer(output[0],new_command)
                # else:
                #     value, error = rap_model.sum_of_variable(command[1],self.repo)
                #     if error:
                #         return "This variable doesnt exist!"
                #     return value

                
            
        return "[COMMAND IS NOT ACCEPTABLE] Eligible commands are FINISH, RESET, SUM, GET_VALUES, LIST, GET, DELETE, ADD, DSUM"

    def __check_input(self, msg):
        """
        checks message input of user
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0].upper()
            if command in ["FINISH", "RESET", "SUM","GET_VALUES" , "LIST" , "GET", "DELETE", "ADD", "SET","DSUM"]:
                return True
            else:
                return False
        else:
            return False

    def look_for_handler(self):
        while self.go:
            self.look_for_peers(6233)
            print(self.peers)
            print("Sleep for 10s")
            time.sleep(10)
            print("Woke up look_for_peers")

    def look_for_peers(self,port):
        
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
                self.peers.append(data)
        except:
            print("Closing")
            sock.close()
        finally:	
            sock.close()


    def look_if_peer_exists(self,server_name_):
        for i in self.peers:
            if i["ServerName"] == server_name_:
                return None, i
        
        return "Error", None
    

    def send_package_to_peer(self,peer_name,command):
        
            error, result=self.look_if_peer_exists(peer_name)
            if error == None:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((result["IP"], result["Port"]))
                res = sock.recv(1024)
                sock.send(command.encode('utf-8'))
                res = sock.recv(1024).decode('utf-8')
                sock.close()

                s = result["ServerName"]
                return f"From server: {s} : {res}", res
            else:
                return f"The {peer_name} doesnt exists!","Error"
    def sstop(self):
        self.go = False
        