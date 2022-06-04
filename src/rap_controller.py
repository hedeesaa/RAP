import rap_model
##

class RAP:

    ERROR_VARIABLE_NOT_EXIST = "[ERROR]: This Variable is not existed!"
    ERROR_ERAP_NOT_ACTIVE = "[ERROR]: ERAP Protocol is Not Active"
    COMMANDS_LIST = ["FINISH", "RESET", "SUM","GET_VALUES" , "LIST" , "GET", "DELETE", "ADD", "SET","DSUM"]

    def __init__(self,*args):
        self.repo = {}
        self.erap = None
        if len(args) == 1:
            self.erap = args[0]
        
    def controller(self, msg):
        if self.__check_input(msg):
            command = msg.split()
            if command[0].upper() == "SET":
                if len(command) == 3:
                    output = command[1].split(".")
                    if len(output) == 2 :
                        if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                        new_command = command[0]+" "+output[1]+" "+command[-1]
                        error, res = self.erap.send_package_to_peer(output[0],new_command)
                        return res.strip()
                    else:
                        error, self.repo=rap_model.set_variable(command[1], int(command[2]),self.repo)
                        if error == False:
                            return "OK"
                return "[ERROR]: SET variable value"

            if command[0].upper() == "ADD":
                if len(command) == 3:
                    output = command[1].split(".")
                    if len(output) == 2:
                        if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                        new_command = command[0]+" "+output[1]+" "+command[-1]
                        error, res = self.erap.send_package_to_peer(output[0],new_command)
                        return  res.strip()
                    else:
                        error, self.repo=rap_model.add_to_variable(command[1], int(command[2]),self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return "OK"
                return "[ERROR]: ADD variable value"

            if command[0].upper() == "DELETE":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                        new_command = command[0]+" "+output[1]
                        error, res = self.erap.send_package_to_peer(output[0],new_command)
                        return  res.strip()
                    else:
                        error, self.repo=rap_model.delete_variable(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return "OK"
                return "[ERROR]: DELETE variable"
                
            if command[0].upper() == "LIST":
                if len(command) == 2:
                    if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                    new_command = command[0]
                    error, res = self.erap.send_package_to_peer(command[1],new_command)
                    return  res.strip()
                else:
                    error, keys=rap_model.list_keys(self.repo)
                    if error == False:
                        return keys

            if command[0].upper() == "GET":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                        new_command = command[0]+" "+output[1]
                        error, res = self.erap.send_package_to_peer(output[0],new_command)
                        return res.strip()
                    else:
                        error, value = rap_model.get_value(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return str(value)
                return "[ERROR]: GET variable"

            if command[0].upper() == "GET_VALUES":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                        new_command = command[0]+" "+output[1]
                        error, res = self.erap.send_package_to_peer(output[0],new_command)
                        return res.strip()
                    else:
                        error, value = rap_model.get_values(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return str(value)
                return "[ERROR]: GET_VALUES variable"
                
            if command[0].upper() == "SUM":
                if len(command) == 2:
                    output = command[1].split(".")
                    if len(output) == 2:
                        if self.erap == None:
                            return RAP.ERROR_ERAP_NOT_ACTIVE
                        new_command = command[0]+" "+output[1]
                        error, res = self.erap.send_package_to_peer(output[0],new_command)
                        return res.strip()
                    else:
                        error, value = rap_model.sum_of_variable(command[1],self.repo)
                        if error:
                            return RAP.ERROR_VARIABLE_NOT_EXIST
                        return value
                return "[ERROR]: SUM variable"

            if command[0].upper() == "RESET":
                if len(command) == 2:
                    if self.erap == None:
                        return RAP.ERROR_ERAP_NOT_ACTIVE
                    new_command = command[0]
                    error, res = self.erap.send_package_to_peer(command[1],new_command)
                    return res.strip()
                else:
                    error, self.repo = rap_model.reset()
                    return "OK"
            
            if command[0].upper() == "FINISH":
                return "FIN"
            
            if command[0].upper() == "DSUM":
                if self.erap == None:
                    return RAP.ERROR_ERAP_NOT_ACTIVE
                command[2] = "including".upper()
                peers = command[command.index('INCLUDING')+1:]

                sums = []
                for peer in peers:
                    new_command = "sum "+command[1]
                    error, res = self.erap.send_package_to_peer(peer,new_command)
                    if error == None:
                        res = res.strip()
                        sums.append(int(res))
                    else:
                        return res.strip()
                return sum(sums)
                
        return f'[COMMAND IS NOT ACCEPTABLE] Eligible commands are {", ".join(RAP.COMMANDS_LIST)}'

    def __check_input(self, msg):
        """
        Checks Message Input of a User
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0].upper()
            if command in RAP.COMMANDS_LIST:
                return True
        return False