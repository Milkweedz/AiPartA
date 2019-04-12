import ast


def tuple_to_string(tupl):
    separator = ","
    tuple_list = []

    for element in tupl:
        tuple_list.append(str(element))

    string = "(" + separator.join(tuple_list) + ")"
    return string


def string_to_tuple(string):
    # literal_eval takes a string and duck types it
    if type(string) is tuple:
        return string
    else :
        #return tuple([x for x in string.strip().split(",")])
        return ast.literal_eval(string)
    #return tupl

#takes two tuples of the same length and subtracts each element. zip returns an iterator
# perhaps can use operator from python? there's operator.add....
def tuple_dif(t1, t2):
    return tuple([x-y for x, y in zip(t1,t2)])

def tuple_add(t1, t2):
    return tuple([x+y for x, y in zip(t1,t2)])

#converts q,r into q,r,s
def tuple2throuple(t):
    if len(t) >2:
        return t
   ### print("{} is {}".format(t, type(t)))
    return (*t,-(t[0]+t[1]))

def throuple2tuple(t):
    return t[:2]

# converts 2-tuple of integer to string 3-tuple
def convert(t):
    return string_to_tuple(tuple2throuple(t))