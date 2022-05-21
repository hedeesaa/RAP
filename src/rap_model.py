def set_variable(variable_, value_,repo__):
    repo__[variable_] = [value_]
    return repo__

def add_to_variable(variable_, value_, repo__):
    error = False
    try:
        repo__[variable_].append(value_)
    except:
        error = True

    print(error)
    
    return repo__, error

def delete_variable(variable_, repo__):
    error = False
    try:
        del repo__[variable_]
    except:
        error = True
    return repo__, error

def list_keys(repo__):
    list_repo = list(repo__.keys())
    return ", ".join(list_repo)

def get_value(variable_,repo__):
    error = False
    try:
        value = repo__[variable_][0]
    except:
        value = 0
        error = True

    return value, error

def get_values(variable_,repo__ ):
    error = False
    try:
        value = repo__[variable_]
    except:
        value = 0
        error = True

    return value, error

def sum_of_variable(variable_,repo__):
    error = False
    try:
        value = sum(repo__[variable_])
    except:
        value = 0
        error = True

    return value, error

def reset():
    return {}
