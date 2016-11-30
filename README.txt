Project: Settlers of Catan
Students: Kelvin Liang, Joey-Michael Fallone
SEC: EB1

Description:

	This is a python version of the popular board game Settlers of Catan
	for all rules please visit http://www.catan.com/service/game-rules)

Instructions:
	4 players, A through D, can play the game!
	run python3 main.py to run the default level.
	for other levels, run main.py 'levelname.lvl'
	there are not currently any other levels... that's in development!
	Following the gui will allow building and interacting with various aspects
	of the game. To interact with the map, simply point and click with the 
	cursor. For example, to build a road one can click on the first node
	and then the second node of where that road travels between.

	One can quickly end a turn by pressing 'e' and may quickly quit the game
	by hitting 'q'

	Remember to check the rules at the url! 

	(A brief rundown if you don't have time to check the url: )


3-4 players compete to gather victory points. First to 10 points wins. 
The board 
layout consists of many different resource tiles such as brick, wood, wheat, 
sheep and stone. 
Numbers between 2-12 are placed on to each resource. This layout is randomly 
chosen. Players take turns rolling dice, whatever is rolled corresponds 
to a number on a resource. If say a 12 is rolled any resource with 12 gives 
players with properties on the tile 1 of that resource. Players use resources 
to build settlements/cities, roads and development cards. Victory points can be
 gained through building settlements, cities, having the longest road, having 
 the largest army, or special development cards. 

At the begining of the game players will take turns to each place two 
settlements anywhere on the board and one road connecting from it. Settlements 
cannot be built within two roads from each other. You place one settlement per 
turn. After this phase the real game begins, players take turns 
rolling the dice, then during your turn you may build/use your resources 
however you want. Trades are permitted with other players so that one
can acquire resources of need. There are many different strategies to the 
game, as one may rely on buying development cards to get victory points
or build the longest road. Initial resource placement is also essential as 
certain resources are more valuable at certain points of the game. One 
more component of the game is the sand tile and the robber. The sand tile is 
an empty space with no resource, it is there to make building around harder.
The robber starts out on this tile. What the robber does is: whenever a 7 is 
rolled the player who's turn it is may move the robber onto any tile on the
board. Whatever tile he chooses will not yield resources to any settlments 
connected to it until it is removed. Finally there are also docks on the 
outside
of the board, each dock specializes in a certain resource or all of them. 
Players can build a settlement at a dock and then gain the ability to trade in
that docks specialty for whatever resource they want however the trade ratios 
are usually 3:1. Common strategy is to control a lot of one resource and its
corresponding dock there are 11 docks in total. 

There are 11 resource tiles all shaped as hexes. 2 hills, 2 fields, 2 forests, 
2 mountains and 2 pastures.
 Forests yield wood, mountains yield stone, 
pastures yield sheep, fields yield wheat and hills yield brick. 

Details:

development cards are bought through having 1 sheep, 1 wheat and 1 stone
they are drawn from a deck

they consist of:

	Knight(makes up largest army) - increase army size by one
	Year of Plenty - lets you pick two of any resource up.
	Monopoly - Choose one resource to have a monopoly of every other player 
	must give up that resource to you
	Road Builder - build two roads free of charge
	University/World wonder - gives the holder 1 victory point
	(player may have multiple)

for longest road - this victory point is given to the player with the longest 
connected road(must be at least 6 roads long)
for largest army - this victory point is given to the player with the most 
knight cards(must have at least 3).

roads are built with: 1 brick, 1 wood
cities are built with: 3 stone, 2 wheat
settlements are built with: 1 brick, 1 wood, 1 sheep, 1 wheat

cities must also be built from settlements(upgrade a settlement)


	
	

Files: 

	Gui.py: 
		contains code to run the interface of the game and essentially runs the
		game as it calls the needed functions to perform tasks as the game goes
		 on. 

	Algorithims.py: 
		contains our main functions that are required to compute data for the
		game such as longest road, largest army, and graph manipulation

	graph.py:
		this is just the graph class code from class, we made use of it to 
		organize our board.

	main.py:
		this code initializes the settings for pygame and
		allows us to run our game, code is largely based
		off the code from the pygame assignment.

	print_numbers:
		contains code for organizing the numbers onto specific tiles, reads in 
		coorindates from a textfile. Also contains functions to organize 
		dictionaries to keep track of what numbers are connected to what 
		resource.

	Build Folder:
		contains the classes for the structures of the game which are roads, 
		settlements and cities. 

	imgs folder:
		contains the images of the settlements, cities and numbers for printing
		 to the board

	maps folder:
		contains map textfiles which hold the coordinates, nodes and edges for 
		board and graphing purposes. For new maps players must add textfiles 
		here and edit the code appropriately. 

	Players Folder:
		contains code for the players class which defines the attribitues for 
		a player

	ResourceCards Folder:
		contains code for each different resource card. Each class has their 
		own functions to apply card effects. 

		folder also contains a deck class which organizes the cards for in 
		game deck use.

	Resources Folder: 
		contains classes for each resource



