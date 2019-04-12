
BASE_SIZE = 3
BLANK_SPACE = ""
COLOUR_KEY = "colour"
PIECES_KEY = "pieces"
BLOCKS_KEY = "blocks"
BLOCKS_STR = "[=]"

import Formatting
from util import dprint, dlprint

board_dict = {}

#give board own dictionary to store board state. set empty board
def init():
    # the dictionary to store these in
    coord_range = range(-BASE_SIZE, BASE_SIZE)
    # create board like in search.py
    for coord in [(q,r) for q in coord_range for r in coord_range if -q-r in coord_range]:
        board_dict[coord] = BLANK_SPACE

# initialises board based on json data
def setup(jsondata):
    init()
    dprint(jsondata.keys())
    colour = jsondata.pop("colour")
    # read through file, add corresponding values to dictionary
    for key in jsondata.keys():
        for i in jsondata[key]:
            dprint(type(i))
            dprint(type(tuple(i)))
            assign_to_board(key, tuple(i), colour)

# takes a key-value pair from json and adds it to board dictionary    
def assign_to_board(key, value, colour):
    
    # sets each coordinate value to current colour
    if key==PIECES_KEY:
        board_dict[value]=colour
    # sets each coord value to block
    elif key==BLOCKS_KEY:
        board_dict[value]=BLOCKS_STR

# returns a tuple of the positions of all the pieces of the given colour
def get_col_coord_tuple(colour):
        return tuple([Formatting.convert(coord) for coord in board_dict if board_dict[coord] == colour])

# returns a dictionary, with coordinates as keys and piece colour as values. so like up to four items.
def get_col_coord_dict(colour):
        #init new dictionary
        new_dict = {}
        for coord in board_dict:
                if board_dict[coord] == colour:
                        new_dict[Formatting.convert(coord)]=colour
        return new_dict

"""
Returns a dictionary of only the pieces on the board, not the blank spaces
I'm sure there's some fancy list comprehension to use here
"""
def get_pieces(stringify = False):
        new_dict = {}
        for x in board_dict.keys():
                if board_dict[x] != BLANK_SPACE:
                        if stringify is True:
                                new_dict[Formatting.tuple_to_string(Formatting.tuple2throuple(x))] = board_dict[x] 
                        else:
                                new_dict[x] = board_dict[x] 
        dlprint(new_dict)
        return new_dict


# changes pieces on the board, or removes them
def update_piece(coords):
        dprint(type(coords))
        dprint(len(coords))
        for x in coords:
                dprint(type(x))
        # just in case, converting from 3-tuple to 2-tuple
        coords = list(map(Formatting.throuple2tuple, coords))
        dprint(coords)
        if len(coords) > 2:
                print("OH WHOOPS YA GOT AN ERROR")
        if len(coords)== 2:
                val = board_dict[coords[0]]
                board_dict[coords[1]] = val
                dprint("new: {}".format(board_dict[coords[1]]))
        # if the piece exits, it just disappears
        board_dict[coords[0]] = BLANK_SPACE
        dprint("original: {}".format(board_dict[coords[0]]))
        
        

def get_board():
    return board_dict