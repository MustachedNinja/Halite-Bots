# First generate the 5 possible moves, 

from hlt.positionals import Position
from hlt.positionals import Direction

possible_pos = []
generatePossibleMoves(ship.position)

TURTLE_RETURN_LIM = 500

def selectFreePos(initial_pos, taken_pos):
    pos_arr = initial_pos.get_surrounding_cardinals()
    pos_arr.append(initial_pos)

    return_arr = []
    for pos in pos_arr:
        if pos not in taken_pos:
            return_arr.append(pos)
    return return_arr

def chooseMoveFromFree(taken_pos, ship, game_map, me)
    pos_arr = selectFreePos(ship.position, taken_pos)
    if ship.halite_amount > TURTLE_RETURN_LIM:
        # Navigate towards the shipyard
        best_pos = findClosest(pos_arr, me.shipyard.position, game_map)
    else:
        # Choose the square with the most halite and go there
        best_pos = None
        best_halite = -1
        for pos in pos_arr:
            compare_halite = game_map[pos].halite_amount
            if compare_halite > best_halite:
                best_halite = compare_halite
                best_pos = pos
    return best_pos
    

def findClosest(pos_arr, destination, game_map):
    best_pos = None
    best_dist = 500
    for pos in pos_arr:
        temp_dist = game_map.calculate_distance(pos, destination)
        if temp_dist < best_dist:
            best_pos = pos
            best_dist = temp_dist
    return best_pos
    
        

