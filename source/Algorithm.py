
import queue

import operator

# specify axes names of the three values in coordinates tuple passed to heuristic()
q,r,s = 0,1,2
board_radius = 3


board = {}
explored_states = {}                         # key: coordinate tuple
fringe_nodes = queue.PriorityQueue()        # nodes that are adjacent to explored nodes, ordered by f(n)


def main():
    global board, explored_states, fringe_nodes
    # board key: coordinate tuple, data: piece color
    # board = {(-3, 0, 3):"r", (-3, 1, 2):"r", (-3, 2, 1):"r", (-3, 3, 0):"r"}
    board_input = {(-3, 0, 3): "r", (-3, 1, 2): "r", (-3, 2, 1): "r", (-3, 3, 0): "r", (-2, -1, 3): "r", (-2, 0, 2): "r", (-2, 1, 1): "r"}
    board.update(board_input)

    global q, r, s
    h = heuristic(((0,0,0),(-1,0,3)), (q,-3))
    print("h(n) = ", h)

    goal = (q,3)

    fringe_nodes.put((24, 0, ((-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0))))
    node_expander(goal)

    while not fringe_nodes.empty():
        print(fringe_nodes.get())

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
    h = int(total_distance/2)+1     # set to 1/2 to account for pieces moving 2 squares by jumping
                                    # int and +1 acts as ceiling function - since you cannot jump off the board
    return h


def node_expander(goal):
    global board_radius
    global board, explored_states, fringe_nodes

    # node is the current state of your pieces on the board, index 1 removes priority value
    node = fringe_nodes.get()                                           # node contains f, g, and state
    g = node[1]                                                         # g = cost of reaching state
    state = node[2]                                                     # state = tuple of piece coordinates
    explored_states[state] = ""
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

        if next_state not in explored_states:
            h = heuristic(coords=next_state, goal=goal)
            # f is estimated total path cost, h is predicted cost of remaining path, g is current path cost
            f = h + g
            fringe_nodes.put((f, g + 1, next_state))

    return None


def path_finder(goal):

    pass


if __name__ == "__main__":
    main()
