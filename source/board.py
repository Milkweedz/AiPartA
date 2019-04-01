
BASE_SIZE = 3
BLANK_SPACE = ""
COLOUR_KEY = "colour"
PIECES_KEY = "pieces"
BLOCKS_KEY = "blocks"
BLOCKS_STR = "[=]"


board_dict = {}

# give board own dictionary to store board state. set empty board
def init():
    # the dictionary to store these in
    coord_range = range(-BASE_SIZE, BASE_SIZE)
    # create board like in search.py
    for coord in [(q,r) for q in coord_range for r in coord_range if -q-r in coord_range]:
        board_dict[coord] = BLANK_SPACE


# initialises board based on json data
def setup(jsondata):
    init()
    # gets colour and removes it from dictionary
    colour = jsondata.pop(COLOUR_KEY)
    # read through file, add corresponding values to dictionary
    for key in jsondata.keys():
        for coord in jsondata[key]:
            assign_to_board(key, tuple(coord), colour)


# takes a key-value pair from json and adds it to board dictionary    
def assign_to_board(key, value, colour):
    
    # sets each coordinate value to current colour
    if key==PIECES_KEY:
        board_dict[value]=colour
    # sets each coord value to block
    elif key==BLOCKS_KEY:
        board_dict[value]=BLOCKS_STR


    

def get_board():
    return board_dict