
import queue
import math
import operator
import time
import itertools


import Formatting       # user defined class in same directory

# specify axes names of the three values in coordinates tuple passed to heuristic()
q,r,s = 0,1,2
board_radius = 3


board = {}
explored_states = {}                        # key: coordinate tuple
fringe_nodes = queue.PriorityQueue()        # nodes that are adjacent to explored nodes, ordered by f(n)
min_f = [None, None]                        # node with minimum f(n). min_f[0] holds f(n) value, min_f[1] holds state

matrix_size = board_radius * 2 + 1
board_matrix = [[None for x in range(matrix_size)] for y in range(matrix_size)]


def main():
    global board, board_matrix, explored_states, fringe_nodes
    # board key: coordinate tuple, data: piece color
    # board_input = {"(-3, 0, 3)":"r", "(-3, 1, 2)":"r", "(-3, 2, 1)":"r", "(-3, 3, 0)":"r"}
    # board_input = {(-3, 0, 3): "r", (-3, 1, 2): "r", (-3, 2, 1): "r", (-3, 3, 0): "r", (-2, -1, 3): "block", (-2, 0, 2): "block", (-2, 1, 1): "block"}
    # board_input = {(-3, 0, 3):"r"}
    board_input = {"(-3, 0, 3)": "r", "(-3, 1, 2)": "r", "(-2, -1, 3)": "block"}
    board.update(board_input)

    # converting board to matrix allows for more efficient code (can access by axes)
    board_matrix = dict_to_matrix(board)

    global q, r, s
    # h = heuristic(((0,0,0),(-1,0,3)), (q,-3))
    # print("h(n) = ", h)

    goal = (q,3)

    # fringe_nodes.put((24, 0, ((-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0)), None))
    fringe_nodes.put((0, 0, ((-3, 0, 3), (-3, 1, 2)), None))
    # fringe_nodes.put((3, 0, ((-3, 0, 3),), None))
    path = path_finder(goal)
    print("# Path: ", path)
    # node_expander(goal)

    # while not fringe_nodes.empty():
    #     print(fringe_nodes.get())

    return None


# coords is a list of 1 to 4 coordinate tuples of pieces
#   coordinate tuple includes 3 axes i.e. q,r,s where s is derived from -q-r
# goal is single tuple consisting of 2 elements: axis (i.e. q,r,s) and value (i.e. -3,3)
def heuristic(coords, goal):
    global board_matrix, q, r, s
    num_pieces = len(coords)
    axes = [q, r, s]
    total_distance = 0      # sum of shortest distances between pieces and their goal
    goal_axis = goal[0]     # axis perpendicular to the side our pieces have to move to
    goal_value = goal[1]    # either -n or n, where n is the radius of the hexagonal board
    #   distinguishes between the two sides perpendicular to the goal_axis

    for coord in coords:
        piece_distance = abs(coord[goal_axis] - goal_value)   # position of piece of goal_axis
        total_distance += piece_distance

    if len(coords) > 1:
        # keep track of steps between pieces
        piece_separation = [[None for i in range(num_pieces)] for j in range(num_pieces)]
        # since we want to move toward one axis (increase or decrease axis value), other two axes must be inversely affected
        axes.remove(goal_axis)
        # p1 and p2 are pieces
        for p1 in range(len(coords)):
            for p2 in range(p1 + 1, len(coords)):
                y_dist = abs(coords[p1][axes[0]] - coords[p2][axes[0]])
                z_dist = abs(coords[p1][axes[1]] - coords[p2][axes[1]])
                # -1 because one piece reaches cross, the other piece sits behind it (from the goal)
                piece_separation[p1][p2] = y_dist + z_dist - 1

        print(piece_separation)
        # combinations = [[[[piece_separation[p1][p2] + piece_separation[p3][p4]
        #                    for p4 in range(len(piece_separation))if piece_separation[p1][p2] is not None
        #                    and piece_separation[p3][p4] is not None
        #                    and p4 not in [p3, p2, p1]]
        #                   for p3 in range(len(piece_separation)) if p3 not in [p2, p1]]
        #                  for p2 in range(len(piece_separation))if p2 not in [p1]]
        #                 for p1 in range(len(piece_separation))]

        combinations = [[piece_separation[p1][p2]
                         for p2 in range(len(piece_separation)) if piece_separation[p1][p2] is not None and p2 != p1]
                        for p1 in range(len(piece_separation))]

        flatten_combinations = combinations
        for i in range(1):
            flatten_combinations = list(itertools.chain.from_iterable(flatten_combinations))

        minsum_separation = min(flatten_combinations)

    # for i in range(len(piece_separation)):
    #     for j in range(len(piece_separation[i])):
    #         if i != j and piece_separation[i][j] is not None:
    #             for k in range(len(piece_separation)):
    #                 for l in range(len(piece_separation[k])):


    # group every 2 pieces together and have them continually jump over each other to goal
    # sum the pair separations of every combination of n pairs of pieces, where n is half of number of pieces (floored)
    # returned as tuple
    # print("GOOSE", piece_separation)
    # combinations = tuple(itertools.combinations(piece_separation, math.floor(num_pieces/2)))
    # for x in combinations:
    #     print(x)
    # sum_separation = map(sum, combinations)
    # print(min(sum_separation), "DEBUG DUCK")

    # # modifier on heuristic value "h(n)"
    # h = total_distance * 1/2 # set to 1/2 to account for pieces moving 2 squares by jumping

    # modifier on heuristic value "h(n)"
        h = math.ceil(total_distance/2) + minsum_separation + num_pieces
    else:
        h = math.ceil(total_distance / 2) + num_pieces
    # h = total_distance  # debug
    print("h= ",h)
    return h


def node_expander(goal):
    # returns the cheapest fringe state that matches goal
    # returns False if no goal-matching state is found
    # "cheats" by using (if h(n)==0) to determine if next_state matches goal, saves having to expand the next_state

    global board_radius
    global board, explored_states, fringe_nodes
    global min_f

    # node is the current state of your pieces on the board, index 1 removes priority value
    node = fringe_nodes.get()                                           # node contains f, g, and state
    g = node[1]                                                         # g = cost of reaching state
    state = node[2]                                                     # state = tuple of piece coordinates
    prev_state = node[3]

    goal_axis = goal[0]     # axis perpendicular to the side our pieces have to move to
    goal_value = goal[1]    # either -n or n, where n is the radius of the hexagonal board

    # stringification needed because strings are always identical if equivalent, tuples are not
    stringified_state = Formatting.tuple_to_string(state)

    # if already explored, discard node
    if stringified_state in explored_states: return False

    # add state to explored states
    if prev_state is None:
        explored_states[stringified_state] = "root"
    else:
        stringified_prev = Formatting.tuple_to_string(prev_state)
        explored_states[stringified_state] = stringified_prev

    moves = [(1,-1,0),(1,0,-1),(0,1,-1),(-1,1,0),(-1,0,1),(0,-1,1)]     # unit vectors of a piece's possible moves
    possible_moves = []                                                 # list of a piece's possible moves
    valid_moves = []                        # list of all possible moves for this turn, minus ones that are not legal

    for piece in state:
        possible_moves.clear()

        # add option to leave board
        if piece[goal_axis] == goal_value:
            valid_moves.append((piece, None))
            continue

        for move in moves:
            new_pos = tuple(map(operator.add, piece, move))  # new_pos is a place the piece can move to
            (q, r, s) = new_pos
            # check that new_pos is in the hexagon
            if abs(q) <= board_radius and abs(r) <= board_radius and abs(s) <= board_radius:
                possible_moves.append(new_pos)

        for move in possible_moves:         # recall that this is one piece's possible moves, not all moves for player
            if new_pos not in board and new_pos not in state:
                valid_moves.append((piece, move))  # recall that this is list of player's all possible moves

    # explore successors of current node, iterate through valid moves
    for choice in valid_moves:
        # choice[0] is original position of piece, index is index of piece in node tuple
        index = state.index(choice[0])
        # if piece not leaving board
        if choice[1] is not None:
            # choice[1] is new position of the piece, next_node is the new state
            next_state = state[:index] + (choice[1],) + state[index+1:]
        else:
            next_state = state[:index] + state[index+1:]

        stringified_next = Formatting.tuple_to_string(next_state)
        if stringified_next not in explored_states:
            h = heuristic(coords=next_state, goal=goal)

            if h == 0:
                explored_states[stringified_next] = Formatting.tuple_to_string(state)
                print("DEBUG4", state)
                # goal has been found
                return next_state

            # f is estimated total path cost, h is predicted cost of remaining path, g is current path cost
            f = h + g
            print(choice, f, g, next_state)
            print(state)
            fringe_nodes.put((f, g + 1, next_state, state))

            if min_f[0] is None or f <= min_f[0]:
                min_f[0] = f
                min_f[1] = next_state

        else:
            print("Already explored")
            print(stringified_next)

    # goal has not been found
    return False


def path_finder(goal):
    current = 0                         # keep track of node resource
    start_time = time.time()            # keep track of time resource

    goal_found = False
    # while time_limit(start_time, limit=2.5) is True:
    while node_limit(current, limit=100) is True:
        # run node_expander i number of times before checking time elapsed
        i = 1000
        while not fringe_nodes.empty() and i > 0:
            goal_found = node_expander(goal)
            if goal_found is not False:
                print("# Goal found")
                print("# ", goal_found)
                node = Formatting.tuple_to_string(goal_found)
                print(explored_states)

                path = []
                while node != "root":
                    path.append(node)
                    node = explored_states[node]
                path.reverse()
                return path

            i -= 1
            print("# Next node")
        current += 1

    # if goal not found, must have reached resource limit
    if goal_found is False:
        print("# Resource limit")

        # node is same as implementation in node_expander
        node = fringe_nodes.get()
        f = node[0]
        if min_f[0] is not None and min_f[0] <= f:
            print(min_f)
        else:
            print(node[2])

    return None


def dict_to_matrix(board):
    size = board_radius * 2 + 1
    # board_matrix = [size][size]
    keys = board.keys()

    for key in keys:
        print(key, "DEBUG")
        coord = Formatting.string_to_tuple(key)
        q, r, s = coord

        board_matrix[q][r] = board[key]

    print(board_matrix)
    return board_matrix


def node_limit(current, limit):
    if current <= limit:
        return True
    else:
        return False


def time_limit(start_time, limit):
    if (time.time() - start_time) >= limit:
        print("# TIME: ", time.time()-start_time)
        return False
    else:
        return True


if __name__ == "__main__":
    main()
