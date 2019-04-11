# Uses the a* algorithm in a given set of nodes to find the optimal path

from search import RED, BLU, GRN
from output import gen_valid_move_norms
from Formatting import *

#receive input. Will need to know (blank spaces, spaces with our pieces, spaces with blocks)
# so this will be just passing the board dictionary to here.
# param: board_dict is a dictionary of the board, with coordinates as keys and blank,colour,block as values
# player_col is the current player's colour
def find_next_step(board_dict, player_col):
    goal_spaces = gen_goal_space(player_col)
    # coordinates of current player pieces
    player_pieces = [x for x in board_dict.keys() if board_dict[x] == player_col]



    return 

# finds shortest path between two hexes with no obstacles
# returns an ordered list of coordinates
def find_short_path(c1, c2):

    return

# calculates "manhattan" distance between two hexes
def dist(c1, c2):

    return

#  A list of coordinates for which the given colour can move off the board
def gen_goal_space(col):
    edge_hexes = gen_valid_move_norms(3)
    index = -1
    if col == RED:
        index = 0
    elif col == GRN:
        index = 1
    elif col == BLU:
        index = 2
    else:
        print("ERROR NOT GOOD COLOUR")
    return [x for x in edge_hexes if x[index]==3]
