"""
Dumb Mining Bot:
Searches for the nearest planet and docks on it
"""
import hlt
import logging

# GAME START
game = hlt.Game("Miner")
logging.info("Starting my Mining bot!")

while True:
    # Update game_map and create and empty command_queue
    game_map = game.update_map()
    command_queue = []

    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue
        
        # Find all planets
        planets = game_map.all_planets()

        # find the closest planet
        best_planet = None
        best_distance = 5000

        for planet in planets:
            if planet.is_owned() or planet.is_full():
                continue
            temp_distance = ship.calculate_distance_between(planet)
            if temp_distance < best_distance:
                best_distance = temp_distance
                best_planet = planet

        if best_planet is not None:
            # If the ship can dock onto the planet, add such a move
            if ship.can_dock(best_planet):
                command_queue.append(ship.dock(best_planet))
            # If not, attempt to move the ship closer to the planet
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(best_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
        else:
            continue

    # Send commands to the game engine
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
