def set_variable(variable_, value_,repo__):
    repo__[variable_] = [value_]
    return repo__

def add_to_variable(variable_, value_, repo__):
    repo__[variable_].append(value_)
    return repo__

def delete_variable(variable_, repo__):
    del repo__[variable_]
    return repo__

def list_keys(repo__):
    list_repo = list(repo__.keys())
    return ", ".join(list_repo)

def get_value(variable_,repo__):
    return repo__[variable_][0]

def get_values(variable_,repo__ ):
    return repo__[variable_]

def sum_of_variable(variable_,repo__):
    return sum(repo__[variable_])

def reset():
    return {}
