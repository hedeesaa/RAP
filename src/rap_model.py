def set_variable(variable_, value_,repo__):
    repo__[variable_] = [value_]
    ## Error, Response
    return False, repo__

def add_to_variable(variable_, value_, repo__):
    error = False
    try:
        repo__[variable_].append(value_)
    except:
        error = True
    return error,repo__

def delete_variable(variable_, repo__):
    error = False
    try:
        del repo__[variable_]
    except:
        error = True
    return error, repo__

def list_keys(repo__):
    list_repo = list(repo__.keys())
    return False, ", ".join(list_repo)

def get_value(variable_,repo__):
    error = False
    try:
        value = repo__[variable_][0]
    except:
        value = 0
        error = True

    return error, value

def get_values(variable_,repo__ ):
    error = False
    try:
        value = repo__[variable_]
    except:
        value = 0
        error = True

    return error, value

def sum_of_variable(variable_,repo__):
    error = False
    try:
        value = sum(repo__[variable_])
    except:
        value = 0
        error = True

    return error, value

def reset():
    return False, {}
