# Uses the a* algorithm in a given set of nodes to find the optimal path

from search import RED, BLU, GRN
from output import gen_valid_move_norms
from Formatting import *

# these are generated once instead of multiple times, saving time
moves_1 = gen_valid_move_norms(1)
moves_2 = gen_valid_move_norms(2)



# receive input. Will need to know (blank spaces, spaces with our pieces, spaces with blocks)
# so this will be just passing the board dictionary to here.
# param: board_dict is a dictionary of the board, with coordinates as keys and blank,colour,block as values
# player_col is the current player's colour
def find_next_step(board_dict, player_col):
    goal_spaces = gen_goal_space(player_col)
    # coordinates of current player pieces
    player_pieces = [x for x in board_dict.keys() if board_dict[x] == player_col]
    print("# board keys: {}".format(board_dict.keys()))
    print("# player pieces: {}".format(player_pieces))
    print("# player colour: {}, equal? {}".format(player_col, RED==player_col))


    # CURRENT ITERATION TO CHANGE
    # find the piece with the shortest distance to goal, move it in a straight line to goal
    coord_pair = min_dist_coords(player_pieces, goal_spaces)
    print("# selected piece, goal position: {}".format(coord_pair))
    
    return "PLACEHOLDER"

# finds shortest path between two hexes with no obstacles
# returns an ordered list of coordinates
def find_short_path(c1, c2, explored=[]):

    # recursive function, so if reached our goal, return
    if c1==c2:
        print("# short path found: {}".format(explored))
        return explored

    # explore all six hexes around, avoiding ones we have already dealt with
    potential_moves = [tuple_add(c1, x) for x in moves_1 if tuple_add(c1, x) not in explored] 

    # only add the next ones to explore that are somehow "closer" to goal
    distances = [tuple_dif(x, c2) for x in potential_moves]
    explored.append(potential_moves[distances.index(min_tuple(distances))])

    return find_short_path(explored[-1], c2, explored)


# finds the "minimum distance" tuple by adding up the absolute value of each element in a tuple, and selecting the minimum tuple from there
# essentially finds the closest tuple to (0,0) from the list
def min_tuple(tuple_list):
    distances = [sum([abs(y) for y in x]) for x in tuple_list]

    # returns the tuple with lowest "distance"
    return tuple_list[distances.index(min(distances))]


# calculates "manhattan" distance between two hexes
def dist(c1, c2):
    # translates the coordinates so that c1 is at (0,0,0), any adjustments to each element to c2 as well
    ####print(tuple_dif(c2, c1))
    return max(abs(x) for x in tuple_dif(c2, c1))


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

# finds the coordinate pair with one item from each list, with minimum distance between coords
def min_dist_coords(piece_list, goal_list):
    # maps each pair to a distance between them
    print("thingos: {}, {}".format(piece_list, goal_list))
    distance_map = [(x, y, dist(x, y)) for x in piece_list for y in goal_list]
    print("# distance maps: {}".format(distance_map))
    # finds the piece-goal pair with the smallest distance
    min_dist = min(x[2] for x in distance_map)
    for x in distance_map:
        if x[2] == min_dist:
            return [x[0], x[1]]
        


