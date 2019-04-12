"""
Formats directions for the next step as necessary

"""

from Formatting import convert, string_to_tuple, tuple_dif
from sys import exit
from util import valid_move, gen_valid_move_norms

MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"
NONE = "NONE"

PLCHOLDER = "????"

# takes a method (MOVE, JUMP, EXIT) beginning coordinate, a destination, and outputs them correctly
def move_to(method, coords):
    src = coords[0]
    # some light error checking
    if coords[0] == None:
        print('HELP'+PLCHOLDER)
        exit()
    
    dst = PLCHOLDER if len(coords)!=2 or coords[1]==None else coords[1]
    if method == EXIT:
        print("{} from {}.".format(EXIT, src))
    else:
        print("{} from {} to {}.".format(method, src, dst))
    # this method is not very python but I've only got so many hours left
    returnlist = [src]
    if (dst != PLCHOLDER):
        returnlist.append(dst)
    return returnlist

# from the change in coordinates, determines if the move is a jump, move, or exit
def determine_move(init_coords, end_coords):
    if init_coords==end_coords:
        print("ERROR, coords are equal! {}={}".format(init_coords, end_coords))
        exit()

    # just in case the coords are passed as a tuple
    if type(init_coords) is tuple:
        init_coords = list(init_coords)
    if type(end_coords) is tuple:

        # if there's only one tuple left in end coords, it'll become a list of integers, so we handle that to make it just a tuple
        if any(end_coords) and type(list(end_coords)[0]) is int:
            end_coords = [end_coords]
        else:
            end_coords = list(end_coords)        
    
    # treats the coordinate lists as sets, uses difference to find the elements that are in one but not the other
    checker=list(set(init_coords)-set(end_coords))+list(set(end_coords)-set(init_coords))

    # clean up list, idk where these errors are coming from atm
    checker = [x for x in checker if type(x) is tuple]
    # checking for type is hugely not the greatest thing
    checker = [convert(x) for x in checker if type(x) is tuple]

    # arguments for the move function at the end. will be changed according to inputs
    move_command = None
    source_coord = checker[0]
    destin_coord = None

    #error handling
    if len(checker)<=0 or len(checker)>2:
        print(checker)
        print(len(checker))
        print("ERROR: Invalid coordinate entry!")
        exit()
        return

    #first, if there is only one element, an exit has been made
    if len(checker)==1 or None in checker:
        move_command = EXIT
        return move_to(move_command, [source_coord[:2]])
    else:
        destin_coord = checker[1]
        
        #now determines if it is a jump, or a move
        if valid_move(2, source_coord, destin_coord):
            move_command = JUMP
        elif valid_move(1, source_coord,destin_coord):
            move_command = MOVE
        else:
            print("ERROR in checking valid move!")
            print(source_coord)
            print(destin_coord)
            return

    # returns 3-tuple to 2-tuple.
    return move_to(move_command, [source_coord[:2], destin_coord[:2]])



