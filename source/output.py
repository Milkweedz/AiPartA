"""
Formats directions for the next step as necessary

"""

import Formatting

MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"
NONE = "NONE"

def gen_valid_move_norms(dist):
    ran = range(-dist,dist+1)
    # list comprehension to generate valid jumps from (0,0,0)
    return [(q,r,s) for q in ran for r in ran for s in ran if q+r+s==0 and (dist in(q,r,s)or-dist in(q,r,s))]

# takes an beginning hex, a destination, and outputs them correctly
def move_to(method, src, dst="????"):
    if method == EXIT:
        return "{} from {}".format(EXIT, src)
    else:
        return "{} from {} to {}".format(method, src, dst)
    print("Error, invalid move formatting!")
    return

# from the change in coordinates, determines if the move is a jump, move, or exit
def determine_move(init_coords, end_coords):
    
    # treats the coordinate lists as sets, uses difference to find the elements that are in one but not the other
    checker=list(set(init_coords)-set(end_coords))+list(set(end_coords)-set(init_coords))

    move_command = None
    source_coord = checker[0]
    destin_coord = None

    #error handling
    if len(checker)<=0 or len(checker)>2:
        print(checker)
        print("ERROR: Invalid coordinate entry!")
        return

    #first, if there is only one element, an exit has been made
    if len(checker)==1:
        print("length of 1")
        move_command = EXIT
    else:
        destin_coord = checker[1]
        #then, determine if a jump or walk. compares the difference of the x and y values of each tuple, and creates a single-element list of either 1|2
        comps = [x-y for x in Formatting.string_to_tuple(checker[0]) for y in Formatting.string_to_tuple(checker[1]) if x-y!=0]
        #this is not completely correct!!!!!!
        if abs(comps[0]) ==2:
            move_command = JUMP
        else:
            move_command = MOVE

    return move_to(move_command, source_coord, destin_coord)

print(move_to("here", "there", MOVE))

