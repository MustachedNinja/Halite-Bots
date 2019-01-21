# The idea behind this bot is it will eat out all the resources near the shipyard
# in the hope that this will allow it to gather resources haster in the early game
# This bot will still move towards the adjacent square with the most halite, but instead of staying until 
# that square no longer has the most halite, it will eat out the resources until that square has virtually no halite left
# This will make moving out of and returning to the shipyard very cheap 
# while also reducing the distance that bots have to travel to gather resources

import hlt

from hlt import constants
from hlt.positionals import Direction
from hlt.positionals import Position

import random
import math
import logging

def findTotalHalite(game_map):
    # Iterate over all map cells and calculate the total halite
    total_halite = 0
    
    for row in range(game_map.height):
        for col in range(game_map.width):
            pos = Position(row, col)
            total_halite += game_map[pos].halite_amount
    return total_halite

""" <<<Game Begin>>> """

game = hlt.Game()

total_halite = findTotalHalite(game.game_map)

game.ready("MyPythonBot")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))



""" <<<Constants>>> """

MAX_REMAINING_HALITE = 50



""" <<<Functions>>> """
# Define all the functions used in this bot


def isStationary(ship, game_map, taken_pos):
    # Determines if a ship is going to stay still this turn
    # Only moves if the ship is full or the position it is at has no more halite to farm
    if ship.is_full:
        return False
    elif not freeSurrounding(ship.position, game_map):
        return True
    elif ship.halite_amount < game_map[ship.position].halite_amount * 0.1:
        return True
    elif game_map[ship.position].halite_amount <= MAX_REMAINING_HALITE:
        return False
    else:
        return True


def freeSurrounding(initial_pos, game_map):
    pos_arr = initial_pos.get_surrounding_cardinals()
    
    for pos in pos_arr:
        if not game_map[pos].is_occupied:
            return True
    return False


def selectMove(taken_pos, ship, game_map, me):
    # Determines best move for a ship to take to get to either the shipyard 
    # or to the square with the most halite
    pos_arr = findFreePos(ship.position, taken_pos)
    total_ship_halite = calculateTotalShipHalite(me, game_map)
    
    if ship.halite_amount > 500:
        best_pos = None
        best_dist = 500
        for pos in pos_arr:
            temp_dist = game_map.calculate_distance(pos, me.shipyard.position)
            if temp_dist < best_dist:
                best_pos = pos
                best_dist = temp_dist
    else:
        best_pos = None
        best_halite = -1
        for pos in pos_arr:
            temp_halite = game_map[pos].halite_amount
            if temp_halite > best_halite:
                best_pos = pos
                best_halite = temp_halite
    return best_pos


def findFreePos(initial_pos, taken_pos):
    # Finds possible moves for a ship to go
    pos_arr = initial_pos.get_surrounding_cardinals()

    return_arr = []
    for pos in pos_arr:
        if pos not in taken_pos:
            return_arr.append(pos)
    return return_arr


def calculateTotalShipHalite(me, game_map):
    # Calculate the halite all the ships can return to the shipyard at this moment, 
    # assuming they dont pick any halite up
    ships = me.get_ships()
    total_halite = 0

    for ship in ships:
        total_halite += ship.halite_amount
#        total_halite -= navigateHomeCost(me.shipyard.position, ship, game_map)
    return total_halite


def navigateHomeCost(destination, ship, game_map):
    # Find the cost for a ship to navigate to a given destination
    # CURRENTLY: this method is extremely expensive 
    
    total_cost = 0
    temp_pos = ship.position

    while temp_pos != destination:
        # Calcualte the cost for moving from this pos
        total_cost += game_map[temp_pos].halite_amount

        # Find the next pos that you are moving to
        pos_arr = temp_pos.get_surrounding_cardinals()
        best_pos = None
        best_dist = 500
        for pos in pos_arr:
            dist = simpleDistance(pos, destination)
            if dist < best_dist:
                best_pos = pos
                best_dist = dist
        temp_pos = best_pos
    return total_cost

def simpleDistance(initial_pos, destination):
    x_dif = initial_pos.x - destination.x
    y_dif = initial_pos.y - destination.y
    return math.sqrt(pow(x_dif, 2) + pow(y_dif, 2))


def shipSpawnRequirement(percent_collected, me, constants, game_map, taken_pos, game):
    if percent_collected > 0.10:
        return False
    elif me.halite_amount < constants.SHIP_COST:
        return False
    elif game_map[me.shipyard].is_occupied:
        return False
    elif percent_collected > 0.15:
        return False
    elif me.shipyard.position in taken_pos:
        return False
    elif not freeSurrounding(me.shipyard.position, game_map):
        return False
    else:
        return True


""" <<<Game Loop>>> """

while True:

    game.update_frame()

    me = game.me
    game_map = game.game_map

    command_queue = []

    collected_total = 0
    taken_pos = []

    all_ships = me.get_ships()
    remove_list = []

    # Filter out the stationary ships first to handle collision avoidance
    for ship in all_ships:
        if isStationary(ship, game_map, taken_pos):
            remove_list.append(ship)
            taken_pos.append(ship.position)
            command_queue.append(ship.stay_still())
            collected_total += game_map[ship.position].halite_amount * 0.25
    
    for ship in remove_list:
        all_ships.remove(ship)
    
    # Find new moves for all the ships which will be moving this turn
    for ship in all_ships:
        new_pos = selectMove(taken_pos, ship, game_map, me)
        taken_pos.append(new_pos)
        command_queue.append(ship.move(game_map.get_unsafe_moves(ship.position, new_pos)[0]))
        collected_total -= game_map[ship.position].halite_amount * 0.1
        
    # Calculate how much we collected
    percent_collected = collected_total / total_halite
    # Update total_halite (since calculating the exact number is too expensive, we are using a rough approximation)
    total_halite -= collected_total * len(game.players)

    # If the percent collected per turn is less than a given percentage and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port.
    if shipSpawnRequirement(percent_collected, me, constants, game_map, taken_pos, game):
        command_queue.append(me.shipyard.spawn())
    
    # Send the command_queue to the game environment and end the turn
    game.end_turn(command_queue)
