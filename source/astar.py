# Uses the a* algorithm in a given set of nodes to find the optimal path

from search import RED, BLU, GRN
from output import gen_valid_move_norms
from Formatting import *

# these are generated once instead of multiple times, saving time
moves_1 = gen_valid_move_norms(1)
moves_2 = gen_valid_move_norms(2)



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
def find_short_path(c1, c2, explored=[]):

    # recursive function, so if reached our goal, return
    if c1==c2:
        print("did it!!!")
        print(explored)
        return explored
    # explore all six hexes around, avoiding ones we have already dealt with
    potential_moves = [tuple_add(c1, x) for x in moves_1 if tuple_add(c1, x) not in explored] 

    # only add the next ones to explore that are somehow "closer" to goal
    """
    print(c1)
    print(c2)
    
    print(tuple_dif(c1, c2))"""
    print(potential_moves)
    
    distances = [tuple_dif(x, c2) for x in potential_moves]

    ####print(min_tuple(distances))
    explored.append(potential_moves[distances.index(min_tuple(distances))])

    find_short_path(explored[-1], c2, explored)

# finds the "minimum distance" tuple by adding up the absolute value of each element in a tuple, and selecting the minimum tuple from there
# essentially finds the closest tuple to (0,0) from the list
def min_tuple(tuple_list):
    distances = [sum([abs(y) for y in x]) for x in tuple_list]

    # returns the tuple with lowest "distance"
    return tuple_list[distances.index(min(distances))]

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
