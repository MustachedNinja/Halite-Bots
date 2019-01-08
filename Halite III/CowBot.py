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


""" <<<Game Begin>>> """

game = hlt.Game()

game.ready("MyPythonBot")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))


""" <<<Constants>>> """

MAX_REMAINING_HALITE = 50

""" <<<Functions>>> """
# Define all the functions used in this bot

def findTotalHalite(game_map):
    # Iterate over all map cells and calculate the total halite
    total_halite = 0
    
    for row in range(game_map.height):
        for col in range(game_map.width):
            pos = Position(row, col)
            total_halite += game_map[pos].halite_amount
    return total_halite


def isStationary(ship, game_map):
    # Determines if a ship is going to stay still this turn
    # Only moves if the ship is full or the position it is at has no more halite to farm
    if ship.is_full:
        logging.info("SHIP FULL")
        return False
    elif ship.halite_amount < game_map[ship.position].halite_amount * 0.1:
        return True
    elif game_map[ship.position].halite_amount <= MAX_REMAINING_HALITE:
        logging.info("EXCEDE MAX" + str(game_map[ship.position].halite_amount))
        return False
    else:
        return True


def selectMove(taken_pos, ship, game_map, me):
    # Determines best move for a ship to take to get to either the shipyard 
    # or to the square with the most halite
    pos_arr = findFreePos(ship.position, taken_pos)
    total_ship_halite = calculateTotalShipHalite(me, game_map)
    
    if total_ship_halite > 1100:
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
    
    total_cost = 0
    temp_pos = ship.position

    while temp_pos is not destination:
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

""" <<<Game Loop>>> """

while True:

    game.update_frame()

    me = game.me
    game_map = game.game_map

    command_queue = []
    # Currently finding total_halite is too expensive
    # total_halite = findTotalHalite(game_map)
    collected_total = 0
    taken_pos = []

    all_ships = me.get_ships()

    logging.info(len(all_ships))

    # Filter out the stationary ships first to handle collision avoidance
    for ship in all_ships:
        if isStationary(ship, game_map):
            all_ships.remove(ship)
            taken_pos.append(ship.position)
            command_queue.append(ship.stay_still())
            collected_total += game_map[ship.position].halite_amount * 0.25
    
    logging.info(len(all_ships))
    
    # Find new moves for all the ships which will be moving this turn
    for ship in all_ships:
        new_pos = selectMove(taken_pos, ship, game_map, me)
        taken_pos.append(new_pos)
        command_queue.append(ship.move(game_map.get_unsafe_moves(ship.position, new_pos)[0]))
        collected_total -= game_map[ship.position].halite_amount * 0.1
        
    
    percent_collected = 0.01
    # Currently finding total_halite is too expensive
    # percent_collected = collected_total / total_halite

    # If the percent collected per turn is less than a given percentage and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port.
    if percent_collected < 0.10 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
    
    # Send the command_queue to the game environment and end the turn
    game.end_turn(command_queue)
