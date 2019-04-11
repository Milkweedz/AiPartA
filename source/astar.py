# Uses the a* algorithm in a given set of nodes to find the optimal path

from util import *
from output import gen_valid_move_norms
from Formatting import *
from sys import exit
import copy

# these are generated once instead of multiple times, saving time
moves_1 = gen_valid_move_norms(1)
moves_2 = gen_valid_move_norms(2)
BOARD_COORDS = moves_1+moves_2+gen_valid_move_norms(3)



# receive input. Will need to know (blank spaces, spaces with our pieces, spaces with blocks)
# so this will be just passing the board dictionary to here.
# param: board_dict is a dictionary of the board, with coordinates as keys and blank,colour,block as values
# player_col is the current player's colour
def find_next_step(board_dict, player_col):
    goal_spaces = gen_goal_space(player_col)
    # coordinates of current player pieces
    player_pieces = [tuple2throuple(x) for x in board_dict.keys() if board_dict[x] == player_col]
    dprint("# board keys: {}".format(board_dict.keys()))
    dprint("# player pieces: {}".format(player_pieces))
    dprint("# player colour: {}, equal? {}".format(player_col, RED==player_col))
    dprint("# goal spaces: {}".format(goal_spaces))


    # CURRENT ITERATION TO CHANGE
    # find the piece with the shortest distance to goal, move it in a straight line to goal
    coord_pair = min_dist_coords(player_pieces, goal_spaces)
    dprint("# selected piece, goal position: {}".format(coord_pair))
    


    path = find_short_path(coord_pair[0], coord_pair[1])
    if len(path)>0:
        # the next step to take is the first element in the path
        return [coord_pair[0], path[0]]
    else: 
        return [coord_pair[0]]

"""
find_short_path
finds shortest path between two hexes with no obstacles
returns an ordered list of coordinates, which are the moves to reach goal
if the goal is reached, returns an empty list
c1 and c2 are initial and destination coordinates, respectively
explored is a list of nodes/hexes that have already been explored
short_path is the current shortest path as a list of coords
"""
def find_short_path(c1, c2, explored=[], short_path = []):

    #error handling
    if None in [c1, c2] or (explored !=[] and short_path==[]) :
        exit()

    # recursive function, so if reached our goal, return
    if c1==c2:
        dprint("# short path found: {}".format(short_path))
        explored.clear()
        fin_path = copy.deepcopy(short_path)
        short_path.clear()
        return fin_path

    # explore all six hexes around, avoiding ones we have already dealt with
    # and marking them as explored
    potential_moves = [tuple_add(c1, x) for x in moves_1 if tuple_add(c1, x) not in explored and tuple_add(c1, x) in BOARD_COORDS] 
    explored.extend(potential_moves)
    dprint("# potential moves: {}".format(potential_moves))
    dprint("explored: {}".format(explored))
    # distances is the subtraction of each tuple in potential_moves from the goal
    # we want to find the smallest distance posible
    distances = [tuple_dif(x, c2) for x in potential_moves]
    dprint("# upper distances: {}".format(distances))
    short_path.append(potential_moves[distances.index(min_tuple(distances))])

    return find_short_path(short_path[-1], c2, explored)


# finds the "minimum distance" tuple by adding up the absolute value of each element in a tuple, and selecting the minimum tuple from there
# essentially finds the closest tuple to (0,0) from the list
def min_tuple(tuple_list):
    dprint("# "+str(tuple_list))
    distances = [sum([abs(y) for y in x]) for x in tuple_list]

    dprint("# sum_distances: {}".format(distances))

    # returns the tuple with lowest "distance"
    return tuple_list[distances.index(min(distances))]


# calculates "manhattan" distance between two hexes
def dist(c1, c2):
    # translates the coordinates so that c1 is at (0,0,0), any adjustments to each element to c2 as well
    ####dprint(tuple_dif(c2, c1))
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
        dprint("ERROR NOT GOOD COLOUR")
    return [x for x in edge_hexes if x[index]==3]

# finds the coordinate pair with one item from each list, with minimum distance between coords
def min_dist_coords(piece_list, goal_list):
    # maps each pair to a distance between them
    dprint("piece list, goal list: {}, {}".format(piece_list, goal_list))
    distance_map = [(x, y, dist(x, y)) for x in piece_list for y in goal_list]
    dprint("# distance maps:")
    dlprint(distance_map)
    # finds the piece-goal pair with the smallest distance
    min_dist = min(x[2] for x in distance_map)
    for x in distance_map:
        if x[2] == min_dist:
            return [x[0], x[1]]
        


