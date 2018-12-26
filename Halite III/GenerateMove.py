# First generate the 5 possible moves, 

from hlt.positionals import Position
from hlt.positionals import Direction

possible_pos = []
generatePossibleMoves(ship.position)

TURTLE_RETURN_LIM = 500

def generatePossiblePos(initial_pos, map):
    return_arr = initial_pos.get_surrounding_cardinals()
    return_arr.append(initial_pos)
    return return_arr

def selectFreePos(pos_arr, taken_pos):
    return_arr = []
    for pos in pos_arr:
        if pos not in taken_pos:
            return_arr.append(pos)
    return return_arr

def chooseMoveFromFree(pos_arr, taken_pos, ship, map, me)
    if ship.halite_amount > TURTLE_RETURN_LIM:
        # Navigate towards a dropoff
        # set best_pos equal to something
    else:
        # Choose the square with the most halite and go there
        best_pos = None
        best_halite = -1
        for pos in pos_arr:
            compare_halite = map[pos].halite_amount
            if compare_halite > best_halite:
                best_halite = compare_halite
                best_pos = pos
    return best_pos
    
    
        

