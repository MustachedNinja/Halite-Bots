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
    for row in game_map.height:
        for col in game_map.width:
            pos = Position(row, col)
            total_halite += game_map[pos].halite_amount
    return total_halite


def isStationary(ship, game_map):
    # Determines if a ship is going to stay still this turn
    # Only moves if the ship is full or the position it is at has no more halite to farm
    if ship.is_full:
        return False
    elif game_map[ship.position].halite_amount <= MAX_REMAINING_HALITE:
        return False
    else:
        return True


def selectMove(taken_pos, ship, game_map, me):
    # Determines best move for a ship to take to get to either the shipyard 
    # or to the square with the most halite

""" <<<Game Loop>>> """

while True:

    game.update_frame()

    me = game.me
    game_map = game.game_map

    

    command_queue = []
    total_halite = findTotalHalite(game_map)
    collected_total = 0
    taken_pos = []

    all_ships = me.get_ships()

    # Filter out the stationary ships first to handle collision avoidance
    for ship in all_ships:
        if isStationary(ship, game_map):
            all_ships.remove(ship)
            taken_pos.append(ship.position)
            command_queue.append(ship.stay_still())
            collected_total += game_map[ship.position].halite_amount * 0.25
    
    # Find new moves for all the ships which will be moving this turn
    for ship in all_ships:
        # Find a new position
        # Add that position to taken_pos
        # Append the new move to command_queue
    
    percent_collected = total_halite / collected_total

    # If the percent collected per turn is less than a given percentage and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port.
    if percent_collected < 0.10 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
    
    # Send the command_queue to the game environment and end the turn
    game.end_turn(command_queue)
