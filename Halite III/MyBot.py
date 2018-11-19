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

    for ship in me.get_ships():
#         If ship is 75% full, move towards dock
#         else: move towards location of greatest halite
        new_position = ship.position
        make_dropoff = False
        if ship.halite_amount > 750:
            # Finds the closest dropoff and sets new_position equal to its position
            dropoffs = me.get_dropoffs()
            if len(dropoffs) == 0:
                make_dropoff == True
            else:
                best_dist = 500
                best_dropoff = dropoffs[0]
                for dropoff in dropoffs:
                    temp_dist = game_map.calculate_distance(ship.position, dropoff.position)
                    if temp_dist < best_dist:
                        best_dist = temp_dist
                        best_dropoff = dropoff
                new_position = best_dropoff.position
        
        elif game.turn_number > 2 and ship.halite_amount < 10:
            new_position = ship.position
        
        else:
            pos_list = ship.position.get_surrounding_cardinals()
            
            best_pos = ship.position
            best_hal = game_map[best_pos].halite_amount
            for pos in pos_list:
#                if game_map[pos].ship == False:
                    temp_hal = game_map[pos].halite_amount
                    if temp_hal > best_hal:
                        best_hal = temp_hal
                        best_pos = pos
            new_position = best_pos
        if make_dropoff == False:
            if new_position == ship.position:
                command_queue.append(ship.stay_still())
            else:
                command_queue.append(ship.move(random.choice(game_map.get_unsafe_moves(ship.position, new_position))))
        else:
            command_queue.append(ship.make_dropoff())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

