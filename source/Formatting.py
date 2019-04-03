import ast


def tuple_to_string(tupl):
    separator = ", "
    tuple_list = []

    for element in tupl:
        tuple_list.append(str(element))

    string = "(" + separator.join(tuple_list) + ")"
    return string


def string_to_tuple(string):
    # literal_eval takes a string and duck types it
    tupl = ast.literal_eval(string)
    return tupl
