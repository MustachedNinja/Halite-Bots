/*
The inspriation behind this bot came from the fact that while CowBot is good at collecting resources, 
it is bad at choosing the optimal path to take to places of large amounts of resources.

This bot while take some time in the first 10 seconds of the game to compute
cost/benefit values for each square of the board, and then update them as the game goes on.
It will also have a variable function for when to spawn ships: If percent of halite collected 
is greater than 0.25, dont spawn a ship.
Also this bot will calculate how much it costs to navigate home. If a bot can return with 1000 halite, it will
Finally, I hope to add dropoff points into this version, so that areas of the map which are close to the spawn point
 and contain at least a certain percentage of the maps resources, a dropoff will be placed there

If a section of size (mapSize/10) has more than x percent of the maps resources build a dropoff there
(assuming that the shipyard is not in that circle)

Consider dropoff located at center of mass and if its closer than mapSize/8 then dont build dropoff
*/

import hlt.*;

import java.util.ArrayList;
import java.util.Random;

public class SmartBot {
    
    /*
    Calculates total halite on the map
    Used only in pre-calculation
    */
    public static void totalHalite(Game game, Player me) {
        GameMap gameMap = game.gameMap;
        int total = 0;
        int totalWeightX = 0;
        int totalWeightY = 0;
        int displacement = gameMap.width / game.players.length;
        int xFin = me.shipyard.position + displacement;
        int xInit = me.shipyard.position - displacement;
        int yFin = me.shipyard.position + displacement;
        int yInit = me.shipyard.position - displacement;        

        for (int row = 0; row < gameMap.width; row++) {
            for (int col = 0; col < gameMap.height; col++) {
                int cellHalite = gameMap[row][col].halite;
                total += cellHalite;
                if (row < xFin && row > xInit && col < yFin && col > yInit) {
                    totalWeightX += cellHalite * col;
                    totalWeightY += cellHalite * row;
                }
            }
        }
        int normalX = totalWeightX / total;
        int normalY = totalWeightY / total;
        Position centerMass = new Position(normalX, normalY);
        return (total, centerMass);
    }

    /*
    Calcualtes the change in halite amount from the previous turn
    Only iterates over all the ships rather than iterating over the entire map
    */
    public static void haliteChange(Game game, GameMap prevMap) {
        players = game.players;
        gameMap = game.gameMap;

        int change = 0;

        for (int i = 0; i < players.length; i++) {
            player = players[i];
            for (int j = 0; j < player.ships.values().length; j++) {
                shipPos = player.ships[j].position;
                // If the ship didn't move
                if (prevMap[shipPos] == gameMap[shipPos]) {
                    change += (int)(prevMap[shipPos].halite * 0.25);
                }
            }
        }

         
        // Return a tuple of totalHalite change and new center of mass
        return change;
    }

    // If time allows, perform center of mass change calculations

    public static void main(final String[] args) {

        Game game = new Game();

        // Precomputing 
        /*
        Here we will calculate:
            total halite
            center of mass

        */
        startingInfo = totalHalite(game, game.me);
        startingHalite = startingInfo[0];
        startingCenter = startingInfo[1];

        // Game start
        game.ready("SmartBot");

        Log.log("Successfully created bot! My Player ID is " + game.myId);

        // Game loop
        for (;;) {
            game.updateFrame();
            final Player me = game.me;
            final GameMap gameMap = game.gameMap;

            final ArrayList<Command> commandQueue = new ArrayList<>();

            ArrayList<Ship> ships = me.ships.values();
            ArrayList<Ship> removeShip = new ArrayList<>();
            ArrayList<Position> takenPos = new ArrayList<>();

            // For each ship
            for (final Ship ship : me.ships.values()) {
                if (isStationary()) {
                    // Add to removeShip
                    // mark position as taken
                }
            }

            game.endTurn(commandQueue);
        }
    }
}
