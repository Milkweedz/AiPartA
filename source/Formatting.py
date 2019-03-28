import ast


def tuple_to_string(tuple):
    separator = ", "
    tuple_list = []

    for element in tuple:
        tuple_list.append(str(element))

    string = "(" + separator.join(tuple_list) + ")"
    return string


def string_to_tuple(string):
    # literal_eval takes a string and duck types it
    tuple = ast.literal_eval(string)
    return tuple
