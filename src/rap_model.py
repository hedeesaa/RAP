# TODO add single node

repo = {}

def set_variable(variable_, value_):
    repo[variable_] = [value_]

def add_to_variable(variable_, value_):
    repo[variable_].append(value_)

def delete_variable(variable_):
    del repo[variable_]

def list_keys():
    return repo.keys()

def get_value(variable_):
    return repo[variable_][0]

def get_values(variable_):
    return repo[variable_]

def sum_of_variable(variable_):
    return sum(repo[variable_])

def reset():
    repo = {}

def controller(msg):
    command = msg.split()
    if command[0] == "SET":
        set_variable(command[1], int(command[2]))
        print(repo)
        return "OK"
    if command[0] == "ADD":
        add_to_variable(command[1], int(command[2]))
        print(repo)
        return "OK"
    if command[0] == "DELETE":
        delete_variable(command[1])
        return "OK"
    if command[0] == "LIST":
        keys=list_keys()
        print(keys)
        return "OK"
    if command[0] == "GET":
        return get_value(command[1])
    if command[0] == "GET_VALUES":
        return get_values(command[1])
    if command[0] == "SUM":
        print(repo)
        return sum_of_variable(command[1])
    if command[0] == "RESET":
        reset()
        return "OK"
    if command[0] == "FINISH":
        return "OK"
    
    
    
