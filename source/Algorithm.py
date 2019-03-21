
#specify axes names of the three values in coordinates tuple passed to heuristic()
q,r,s = 0,1,2

def main():
    global q, r, s
    h = heuristic(((0,0,0),), (q,-3))
    print(h, "DEBUG")

    return None



#coords is a list of 1 to 4 coordinate tuples of pieces
#   coordinate tuple includes 3 axes i.e. q,r,s where s is derived from -q-r
#goal is single tuple consisting of 2 elements: axis (i.e. q,r,s) and value (i.e. -3,3)
def heuristic(coords, goal):
    total_distance = 0      #sum of shortest distances between pieces and their goal
    goal_axis = goal[0]     #axis perpendicular to the side our pieces have to move to
    goal_value = goal[1]    #either -n or n, where n is the radius of the hexagonal board
                            #   distinguishes between the two sides perpendicular to the goal_axis


    for coord in coords:
        print(coords, "DEBUG")
        piece_distance = abs(coord[goal_axis] - goal_value)   #position of piece of goal_axis
        total_distance += piece_distance


    #modifier on heuristic value "h(n)"
    h = int(total_distance/2)+1     #set to 1/2 to account for pieces moving 2 squares by jumping
                                    #int and +1 acts as ceiling function - since you cannot jump off the board


    return h





if __name__ == "__main__":
    main()