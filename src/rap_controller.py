import rap_model
class RAP:
    def __init__(self, id):
        self.id = id
        self.repo = {}
    def controller(self, msg):
        if self.__check_input(msg):
            command = msg.split()
            
            if command[0] == "SET":
                self.repo=rap_model.set_variable(command[1], int(command[2]),self.repo)
                return "OK"

            if command[0] == "ADD":
                self.repo=rap_model.add_to_variable(command[1], int(command[2]),self.repo)
                return "OK"

            if command[0] == "DELETE":
                self.repo=rap_model.delete_variable(command[1],self.repo)
                return "OK"

            if command[0] == "LIST":
                keys=rap_model.list_keys(self.repo)
                return keys

            if command[0] == "GET":
                return str(rap_model.get_value(command[1],self.repo))

            if command[0] == "GET_VALUES":
                return str(rap_model.get_values(command[1],self.repo))
                
            if command[0] == "SUM":
                return rap_model.sum_of_variable(command[1],self.repo)

            if command[0] == "RESET":
                self.repo = rap_model.reset()
                return "OK"
            
            if command[0] == "FINISH":
                return "FIN"
            
        return "[COMMAND IS NOT ACCEPTABLE] Eligible commands are FINISH, RESET, SUM, GET_VALUES, LIST, GET, DELETE, ADD"

    def __check_input(self, msg):
        """
        checks message input of user
        Returns True or False
        """
        if isinstance(msg, str):
            command = msg.split()[0]
            if command in ["FINISH", "RESET", "SUM","GET_VALUES" , "LIST" , "GET", "DELETE", "ADD", "SET"]:
                return True
            else:
                return False
        else:
            return False

        
        


        