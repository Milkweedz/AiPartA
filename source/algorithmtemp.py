import queue
import math
import operator
import time
import itertools

from util import dprint


# Variables and constants used for calculations
board_radius = 3

# dictionary to store all current/simulated board spaces that are not blank
board_items = {}

#will contain all explored states. Key:coordinate tuple, Val: explored yes/no
explored_states={}

# Nodes that are adjacent to explored nodes, ordered by f(n), where f(n) is the TODO!!!!!!
fringe_nodes = queue.PriorityQueue()

# node with minimum f(n). min_f[0] holds f(n) value, min_f[1] holds state
# so essentially the best choice we have at that time
min_f = [None, None]                        

# A Matrix to store all the hexes in a grid-like fashion, since they can be represented with only 2 coordinates
matrix_size = board_radius * 2 + 1
board_matrix = [[None for x in range(matrix_size)] for y in range(matrix_size)]



"""
Attempt to transfer the work Jay did into this algorithm so that things work
"""
def temp(initial_state, my_pieces, goal):
    
    # store information on where each piece is, and where each block is. I think we get that earlier and can check for board with BOARD_COORDS

    # convert the dictionary into a 2x2 matrix, faster access, and is useful with only needing x and y

    # q, r, s = 0, 1, 2. These represent edgeds that we need to reach IDK WHAT GOAL IS OR IS FOR. goal[0] is the goal edge, but what is goal[1]???

    # add the starting nodes to the front of the priorityqueue. the first two zeroes are the priority, the None is the timeout

    # timing because we like to optimise
    start_time = time.time()

    # get next move: takes a dictionary of all the non-blank spaces on the board, a tuple of all our pieces, and our goal (i think goal[1] might be the max heuristic from the start???)
    # returns an entire path, so we may need to disassemble that to one at a time to output correctly
    get_next_move(initial_state, my_pieces, goal)


    end_time = time.time()

    dprint("Time taken: {}".format(end_time-start_time))

    return

"""
TODO IDK WHAT THIS DOES REALLY BUT WE'LL SEE
"""
def get_next_move(board_dict, my_pieces, goal):
    board = board_dict
    
    return