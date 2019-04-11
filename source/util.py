RED = "red"
BLU = "blue"
GRN = "green"

DEBUG = False

from Formatting import *

# debug printer
def dprint(s):
    if DEBUG:
        print("# {}".format(s))
    return

def dlprint(s):
    if DEBUG:
        print(*s,sep='\n')
    return

# checks if a particular move dist away is a valid move to dest coord
def valid_move(dist, coord1, coord2):
    return bool(tuple_dif(coord1, coord2) in gen_valid_move_norms(dist)) 


def gen_valid_move_norms(dist):
    ran = range(-dist,dist+1)
    # list comprehension to generate valid jumps from (0,0,0)
    return [(q,r,s) for q in ran for r in ran for s in ran if q+r+s==0 and (dist in(q,r,s)or-dist in(q,r,s))]
    