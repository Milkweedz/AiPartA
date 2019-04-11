RED = "red"
BLU = "blue"
GRN = "green"

DEBUG = True


# debug printer
def dprint(s):
    if DEBUG:
        print("# {}".format(s))
    return

def dlprint(s):
    if DEBUG:
        print(*s,sep='\n')
    return
    