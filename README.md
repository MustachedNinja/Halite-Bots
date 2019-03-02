# Halite-bots
Experimenting with different bots for the halite.io competition

This is a collection of bots I used for all the Halite competitions
<hr>
<h3>Halite 3 </h3>
<p>
I started by writing SimpleBot1 to test out various methods of collision avoidance, and just solving very basic problems to familiarize myself with the functions available. SimpleBot1 chose to move to the square directly adjacent to it which had the most halite, mostly regardless of all other factors. This proved a problem when two squares had the same amount of resources, making the bot waste resources moving between them. SimpleBot1 placed #2700 on average.

Instead of trying to fix minimal issues in SimpleBot1 I decided to drop it and write a new bot. This one was titled CowBot because the basic idea of the ships was to select a square directly adjacent to them and stay on that square until that square had less than 50 resources (at which point resources collected per turn were miniscule and would waste time). This proved extremely effective and even without bug fixes this bot placed #1600. There were multiple issues since the ships would stay still therefore collision avoidance had to be more detailed and handle more cases. The main source of bugs were when the shipyard or another ship was completely surrounded by ships, but I managed to fix most of the bugs. After bug fixes the bot placed in #900.

At this point I saved my progress to CowBotv1 which is what I ended up using as my final bot, and continued experimenting in the original CowBot file. However, after adding more complicated decision-making which relied more on calculating various map values, I realized python was too slow for my purposes so I decided to switch to Java. 

I started the Java bot a day before the end of the competition, so I was unable to finish it in time. The basic idea was that in the 10 second section before the start of the game, the bot would calculate the center of mass of resources for my fourth of the screen, as well as total halite. If the center of mass was farther than 10 spaces away from the shipyard, then as soon as the ships get enough halite, they will spawn a shipyard at the center of mass. While the game is going on, the center of mass is updated and once it becomes outside of the 10-square distance, a shipyard is spawned at that location. The idea behind this is that the center of mass should be the closest distance from the maximum amount of resources, which should theoretically allow for a faster resource gathering rate.
</p>
