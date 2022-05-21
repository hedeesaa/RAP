import rap_model
class RAP:
    def __init__(self, id):
        self.id = id
        self.repo = {}
    def controller(self, msg):
        if self.__check_input(msg):
            command = msg.split()
            
            if command[0].upper() == "SET":
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

        
        


        