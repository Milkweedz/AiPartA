
import queue
import math
import operator

import Formatting       # user defined class in same directory

# specify axes names of the three values in coordinates tuple passed to heuristic()
q,r,s = 0,1,2
board_radius = 3


board = {}
explored_states = {}                        # key: coordinate tuple
fringe_nodes = queue.PriorityQueue()        # nodes that are adjacent to explored nodes, ordered by f(n)
min_f = [None, None]                        # node with minimum f(n). min_f[0] holds f(n) value, min_f[1] holds state


def main():
    global board, explored_states, fringe_nodes
    # board key: coordinate tuple, data: piece color
    board_input = {(-3, 0, 3):"r", (-3, 1, 2):"r", (-3, 2, 1):"r", (-3, 3, 0):"r"}
    # board_input = {(-3, 0, 3): "r", (-3, 1, 2): "r", (-3, 2, 1): "r", (-3, 3, 0): "r", (-2, -1, 3): "block", (-2, 0, 2): "block", (-2, 1, 1): "block"}
    # board_input = {(-3, 0, 3):"r"}
    # board_input = {(-3, 0, 3): "r", (-3, 1, 2): "r", (-2, -1, 3): "block"}
    board.update(board_input)

    global q, r, s
    # h = heuristic(((0,0,0),(-1,0,3)), (q,-3))
    # print("h(n) = ", h)

    goal = (q,3)

    fringe_nodes.put((24, 0, ((-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0)), None))
    # fringe_nodes.put((24, 0, ((-3, 0, 3), (-3, 1, 2)), None))
    # fringe_nodes.put((3, 0, ((-3, 0, 3),), None))
    path_finder(goal)
    # node_expander(goal)

    # while not fringe_nodes.empty():
    #     print(fringe_nodes.get())

    return None


# coords is a list of 1 to 4 coordinate tuples of pieces
#   coordinate tuple includes 3 axes i.e. q,r,s where s is derived from -q-r
# goal is single tuple consisting of 2 elements: axis (i.e. q,r,s) and value (i.e. -3,3)
def heuristic(coords, goal):
    total_distance = 0      # sum of shortest distances between pieces and their goal
    goal_axis = goal[0]     # axis perpendicular to the side our pieces have to move to
    goal_value = goal[1]    # either -n or n, where n is the radius of the hexagonal board
                            #   distinguishes between the two sides perpendicular to the goal_axis

    for coord in coords:
        piece_distance = abs(coord[goal_axis] - goal_value)   # position of piece of goal_axis
        total_distance += piece_distance

    # modifier on heuristic value "h(n)"
    h = math.ceil(total_distance * 1/2) # set to 1/2 to account for pieces moving 2 squares by jumping
                                        # int and +1 acts as ceiling function - since you cannot jump off the board

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

        for move in moves:
            new_pos = tuple(map(operator.add, piece, move))  # new_pos is a place the piece can move to
            (q, r, s) = new_pos
            if abs(q) <= 3 and abs(r) <= 3 and abs(s) <= 3:            # check that new_pos is in the hexagon
                possible_moves.append(new_pos)

        for move in possible_moves:         # recall that this is one piece's possible moves, not all moves for player
            if move not in board:
                valid_moves.append((piece, move))  # recall that this is list of player's all possible moves

    # explore successors of current node, iterate through valid moves
    for choice in valid_moves:
        # choice[0] is original position of piece, index is index of piece in node tuple
        index = state.index(choice[0])
        # choice[1] is new position of the piece, next_node is the new state
        next_state = state[:index] + (choice[1],) + state[index+1:]

        stringified_next = Formatting.tuple_to_string(next_state)
        if stringified_next not in explored_states:
            h = heuristic(coords=next_state, goal=goal)

            if h == 0:
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
    # resource limit (number of nodes explored)
    limit = 10000

    while not fringe_nodes.empty() and limit > 0:
        goal_found = node_expander(goal)
        if goal_found is not False:
            print("Goal found")
            print(goal_found)
            break
        limit -= 1
        print(next)

    # if goal not found, limit must have reached 0
    if limit <= 0:
        print("Resource limit")

        # node is same as implementation in node_expander
        node = fringe_nodes.get()
        f = node[0]
        if min_f[0] <= f:
            print(min_f[1])
        else:
            print(node[2])


if __name__ == "__main__":
    main()
