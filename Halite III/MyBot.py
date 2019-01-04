#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import Position

# This library allows you to generate random numbers.
import random


# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

TURTLE_RETURN_LIM = 500

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """



def selectFreePos(initial_pos, taken_pos):
    pos_arr = initial_pos.get_surrounding_cardinals()
    pos_arr.append(initial_pos)

    return_arr = []
    for pos in pos_arr:
        if pos not in taken_pos:
            return_arr.append(pos)
    return return_arr

def chooseMoveFromFree(taken_pos, ship, game_map, me):
    pos_arr = selectFreePos(ship.position, taken_pos)
    if ship.halite_amount > TURTLE_RETURN_LIM:
        # Navigate towards the shipyard
        best_pos = findClosest(pos_arr, me.shipyard.position, game_map)
        if ship.position is me.shipyard.position:
            best_pos = ship.position
    elif ship.halite_amount < (game_map[ship.position].halite_amount * 0.1):
        best_pos = ship.position
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

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    taken_pos = []

    for ship in me.get_ships():
    
        new_position = chooseMoveFromFree(taken_pos, ship, game_map, me)
        
        taken_pos.append(new_position)
        
        if new_position == ship.position:
            command_queue.append(ship.stay_still())
        else:
            command_queue.append(ship.move(game_map.get_unsafe_moves(ship.position, new_position)[0]))


    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)


