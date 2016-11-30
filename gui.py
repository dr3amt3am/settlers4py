import sys, pygame
from pygame.sprite import LayeredUpdates
from collections import namedtuple
import random # for dice
import time
from Players.players import Player
from ResourceCards.cards import *
import print_numbers
#import algorithims 
from graph import *
from Build.settlement import *
from algorithims import *
#from sounds import SoundManager
from Build.city import *

'''
Please note much of this code is based upon
the code given for assignment #2

This is essentially a very very heavily modified
version of gui.py from that assignment. So much so 
modified that only select parts are used.
'''

# Sound names 
SELECT_SOUND = "Select"
BUTTON_SOUND = "Button"

# Visual size information
MAP_WIDTH = 711
BAR_WIDTH = 200
BUTTON_HEIGHT = 50
CENTER = 100

# initialize fonts
pygame.font.init()
FONT_SIZE = 16
BIG_FONT_SIZE = 42
FONT = pygame.font.SysFont("Arial", FONT_SIZE)
BIG_FONT = pygame.font.SysFont("Arial", BIG_FONT_SIZE)
BIG_FONT.set_bold(True)

# padding for the left and top side of the bar
PAD = 6

# Blink speed
RETICLE_RATE = 0.02

# Names for the different players
PLAYER_NAME = {
	0: "Player A",
	1: "Player B",
	2: "Player C",
	3: "Player D"

}

# RGB for GUI
FONT_COLOR = (0, 0, 0)
BAR_COLOR = (150, 150, 150)
OUTLINE_COLOR = (50, 50, 50)
BUTTON_HIGHLIGHT_COLOR = (255, 255, 255)
BUTTON_DISABLED_COLOR = (64, 64, 64)

class Modes:
	# this is just a draft. Likely needs changing
	Roll, RollDisplay, Action, Trade, ResSel1, ResSel2, ValSel1, ValSel2, \
	YesNo, Build, BuildRoad, RoadInter, BuildCity, BuildSettlement, BuildCard,\
	UseCard, DrawCard, InvtCheck, Plenty, Monopoly, GameOver = range(21)


# button container class
Button = namedtuple('Button', ['slot', 'text', 'onClick', 'condition'])

class GUI(LayeredUpdates):

	num_instances = 0

	# any functions that are needed for init should go here

	def __init__(self, screen_rect, bg_color):
		
		LayeredUpdates.__init__(self) # super class
		if GUI.num_instances != 0:
			raise Exception("GUI: One game at a time please!")
		GUI.num_instances = 1 # flag init has been called

		# keep track of turn number
		self.turn = {each_player: 0 for each_player in PLAYER_NAME}
		self._curr_player = 0 # player index, start with A
		self._dice = 0
		self._value = 0
		# create player objects 
		self.player_list = {each_player: Player(each_player) for each_player in PLAYER_NAME}

		# lists of roads for each player (edges in tuples)
		self.road0 = list()
		self.road1 = list()
		self.road2 = list()
		self.road3 = list()


		# create deck
		self.deck = Deck()
		self.deck.shuffle()

		self.cardflag = 0

		# active settlements and cities that need to be drawn
		self.active_settlements = dict()
		self.active_cities = dict()
		self.active_nodes = list()

		# set up the screen
		self.screen = pygame.display.set_mode((screen_rect.w, screen_rect.h))
		self.screen_rect = screen_rect

		self.build_package = {'type': None, 'x': None, 'y': None}

		# board game image 
		self.board = pygame.image.load('board.jpg')

		# the rect containing the info bar
		self.bar_rect = pygame.Rect(screen_rect.w - BAR_WIDTH,
									0,
									BAR_WIDTH,
									screen_rect.h)

		# the rect containing the board view
		self.view_rect = pygame.Rect(0, 
									 0, 
									 MAP_WIDTH,
									 screen_rect.h)
		self.bg_color = bg_color
		self.map = None

		self._trade_pack1 = {'res_type': None, 'number': 0}
		self._trade_pack2 = {'res_type': None, 'number': 0}

		# Set up team information
		self.num_players = 4 # always four players for now
		self.current_turn = 0
		self.win_player = None

		self.roll_button = Button(0, "Roll Dice", self.roll_click, None)
		self.ok_button = Button(0, "Sounds good!", self.back_to_act, None)

		# some more visual setup
		# this list is for action mode
		self.buttons = [ # these require functinos to be added
		# see struct of button args: 'slot', 'text', 'onClick', 'condition'
		Button(0, "End Turn", self.end_turn, None), 
		Button(1, "Build", self.build_start, self.has_started), 
		Button(2, "Trade", self.propose_trade, self.has_started),
		Button(4, "Card", self.cardmode, self.can_build_card),
		Button(3, "Inventory", self.check_inventory, None)

		]

		self.tradewith = [ # list all the player names here as buttons
			Button(0, 'Go Back', self.back_to_act, None),
			Button(4, 'Player A', self.trade_withA, self.can_tradeA),
			Button(3, 'Player B', self.trade_withB, self.can_tradeB),
			Button(2, 'Player C', self.trade_withC, self.can_tradeC),
			Button(1, 'Player D', self.trade_withD, self.can_tradeD),
		]

		self.resources1 = [ # list all the possible resources here as buttons
			Button(0, 'Wood', self.trade_wood1, None),
			Button(1, 'Wheat', self.trade_wheat1, None),
			Button(2, 'Brick', self.trade_brick1, None),
			Button(3, 'Sheep', self.trade_sheep1, None),
			Button(4, 'Stone', self.trade_stone1, None)
		]

		self.resources2 = [ # list all the possible resources here as buttons
			Button(0, 'Wood', self.trade_wood2, None),
			Button(1, 'Wheat', self.trade_wheat2, None),
			Button(2, 'Brick', self.trade_brick2, None),
			Button(3, 'Sheep', self.trade_sheep2, None),
			Button(4, 'Stone', self.trade_stone2, None)
		]

		self.numbers1 = [ # use up or down buttons to change values
		Button(2, 'More', self.up1, self.go_more1), # eventually need to add cond.
		Button(1, 'Less', self.down1, self.greater_than_zero),
		Button(0, 'Done', self.done1, self.greater_than_zero)
		]

		self.numbers2 = [ # use up or down buttons to change values
		Button(2, 'More', self.up1, self.go_more2), # eventually need to add cond.
		Button(1, 'Less', self.down1, self.greater_than_zero),
		Button(0, 'Done', self.done2, self.greater_than_zero)
		]

		self.construction = [ # list of buttons of items one can build
		Button(0, "Go Back", self.back_to_act, self.has_started),
		Button(1, 'Road', self.build_road, self.can_build_road),
		Button(2, 'Settlement', self.build_settlement, self.can_build_set),
		Button(3, 'City', self.build_city, self.can_build_city),
		]

		self.yesno = [ # yes or no!
			Button(0, "NAY!", self.noway, None),
			Button(1, "YAY!", self.yesway, None) # add conditions for yes?
		]

		self.card_choices = [
		Button(0, "Go Back", self.back_to_act, None),
		Button(1, "Buy (draw)", self.buy_card, self.can_buy_card), 
		# 1 wheat 1 stone 1 sheep
		Button(2, "Use", self.use_card, self.has_card)]

		self.use_cards = [
		Button(0, "Go Back", self.back_to_act, None),
		Button(1, "World Wonder", self.use_wonder, self.has_wonder),
		Button(2, "Road Builder", self.use_roadbuilder, self.has_roadbuilder),
		Button(3, "Knight", self.use_knight, self.has_knight),
		Button(4, "Year of Plenty", self.use_year_plenty, self.has_year_plenty),
		Button(5, "Monopoly", self.use_monopoly, self.has_monopoly)
		]

		self.plenty_buttons = [
		Button(0, "Wheat", self.plenty_wheat, None),
		Button(1, "Stone", self.plenty_stone, None), 
		Button(2, "Brick", self.plenty_brick, None),
		Button(3, "Wood", self.plenty_wood, None),
		Button(4, "Sheep", self.plenty_sheep, None)]

		self.monopoly_buttons = [
		Button(0, "Wheat", self.monopoly_wheat, None),
		Button(1, "Stone", self.monopoly_stone, None),
		Button(2, "Brick", self.monopoly_brick, None),
		Button(3, "Wood", self.monopoly_wood, None),
		Button(4, "Sheep", self.monopoly_sheep, None)]

		self.game_over = Button(0, "Exit", self.gtfo, None)
		
		
		self.player_list[self._curr_player]._wheat = 10000
		self.player_list[self._curr_player]._stone = 10000
		self.player_list[self._curr_player]._brick = 10000
		self.player_list[self._curr_player]._sheep = 10000
		self.player_list[self._curr_player]._wood = 10000

		self.player_list[1]._wheat = 10000
		self.player_list[1]._stone = 10000
		self.player_list[1]._brick = 10000
		self.player_list[1]._sheep = 10000
		self.player_list[1]._wood = 10000
		
		# start mode
		self.mode = Modes.Build

		# victory point info
		self.largest_army = None
		self.longest_road = 4
		self.longest_road2 = None
		self.longest_road_length = 0


	# great function to see if we've pass the first two turns.
	# will be used in many areas
	def has_started(self):
		if self.turn[self._curr_player] < 2:
			return False
		return True

	# some specific on-click functions for buttons 
	# not from a2

	def check_inventory(self):
		self.mode = Modes.InvtCheck

	def can_build_card(self):
		if len(self.player_list[self._curr_player]._cards) == 0:
			# then try can buy card
			return self.can_buy_card()
		else:
			return True

	def back_to_act(self):
		self.mode = Modes.Action

	def roll_click(self):
		'''
		Rolls the (2) die and prints the value to the screen. Then returns 
		the aforementioned value.
		'''
		# pseudo random roll
		# two dice are used because larger numbers are supposed to have a 
		# higher probability for gameplay. This will simulate a real life
		# roll with 2 die.
		dice1 = random.randint(1, 6)
		dice2 = random.randint(1, 6)
		# add the two numbers together
		self._dice = dice1 + dice2

		# return roll #
		return self._dice

	def trade_wood1(self):
		self._trade_pack1['res_type'] = 'wood'
		self.mode = Modes.ValSel1

	def trade_wheat1(self):
		self._trade_pack1['res_type'] = 'wheat'
		self.mode = Modes.ValSel1

	def trade_brick1(self):
		self._trade_pack1['res_type'] = 'brick'
		self.mode = Modes.ValSel1

	def trade_sheep1(self):
		self._trade_pack1['res_type'] = 'sheep'
		self.mode = Modes.ValSel1

	def trade_stone1(self):
		self._trade_pack1['res_type'] = 'stone'
		self.mode = Modes.ValSel1

	def trade_wood2(self):
		self._trade_pack2['res_type'] = 'wood'
		self.mode = Modes.ValSel2

	def trade_wheat2(self):
		self._trade_pack2['res_type'] = 'wheat'
		self.mode = Modes.ValSel2

	def trade_brick2(self):
		self._trade_pack2['res_type'] = 'brick'
		self.mode = Modes.ValSel2

	def trade_sheep2(self):
		self._trade_pack2['res_type'] = 'sheep'
		self.mode = Modes.ValSel2

	def trade_stone2(self):
		self._trade_pack2['res_type'] = 'stone'
		self.mode = Modes.ValSel2

	def gtfo(self):
		quit()

	def propose_trade(self):
		'''
		Changes to Trade mode	
		'''
		self.mode = Modes.Trade

	def can_tradeA(self):
		a = (self._curr_player == 0)
		return not a

	def can_tradeB(self):
		a = (self._curr_player == 1)
		return not a

	def can_tradeC(self):
		a = (self._curr_player == 2)
		return not a

	def can_tradeD(self):
		a = (self._curr_player == 3)
		return not a

	def can_buy_card(self):
		return (self.player_list[self._curr_player].wheat >= 1 and 
			   self.player_list[self._curr_player].stone >=1 and 
			   self.player_list[self._curr_player].sheep >= 1)

	def can_build_road(self):
		if not self.has_started():
			return False
		elif self.player_list[self._curr_player].brick > 0 and \
			 self.player_list[self._curr_player].wood > 0:
			 return True

	def has_card(self):
		if len(self.player_list[self._curr_player]._cards) > 0:
			return True

		return False

	def go_more1(self):
		# time to check for resource types..........
		if self._trade_pack1['res_type'] is 'stone':
			return self.player_list[self._curr_player]._stone > self._value
		elif self._trade_pack1['res_type'] is 'wheat':
			return  self.player_list[self._curr_player]._wheat > self._value
		elif self._trade_pack1['res_type'] is 'wood':
			return self.player_list[self._curr_player]._wood > self._value
		elif self._trade_pack1['res_type'] is 'sheep':
			return self.player_list[self._curr_player]._sheep > self._value
		elif self._trade_pack1['res_type'] is 'brick':
			return self.player_list[self._curr_player]._brick > self._value

	def go_more2(self):
		# time to check for resource types..........
		if self._trade_pack2['res_type'] is 'stone':
			return self.player_list[self.send_to]._stone > self._value
		elif self._trade_pack2['res_type'] is 'wheat':
			return  self.player_list[self.send_to]._wheat > self._value
		elif self._trade_pack2['res_type'] is 'wood':
			return self.player_list[self.send_to]._wood > self._value
		elif self._trade_pack2['res_type'] is 'sheep':
			return self.player_list[self.send_to]._sheep > self._value
		elif self._trade_pack2['res_type'] is 'brick':
			return self.player_list[self.send_to]._brick > self._value

	def trade_withA(self):
		'''
		Accepts which user you are sending it to, will then change to 
		intermediary trade mode
		'''
		self.send_to = 0
		self.mode = Modes.ResSel1

	def trade_withB(self):
		'''
		Accepts which user you are sending it to, will then change to 
		intermediary trade mode
		'''
		self.send_to = 1
		self.mode = Modes.ResSel1

	def trade_withC(self):
		'''
		Accepts which user you are sending it to, will then change to 
		intermediary trade mode
		'''
		self.send_to = 2
		self.mode = Modes.ResSel1

	def trade_withD(self):
		'''
		Accepts which user you are sending it to, will then change to 
		intermediary trade mode
		'''
		self.send_to = 3
		self.mode = Modes.ResSel1

	def end_turn(self):
		'''
		Function that is called when the end turn button is clicked. 
		Simply changes CURR_PLAYER and mode back to roll!
		'''
		self.mode = Modes.Roll
		self.turn[self._curr_player] += 1
		if self._curr_player is 3:
			self._curr_player = 0
		else:
			self._curr_player += 1

		if self.has_started():
			# normal turn
			self.mode = Modes.Roll
		else:
			# still in initial building mode
			self.mode = Modes.Build
		# check who has largest army
		#largest_army2 = largest_army(self.player_list, largest_army)
		# check who has the longest road
		#longest_road2 = longest_road()

		# if largest army has changed 
		# subtract victory pts from player who lost it
		# add victory pts to player who gained it
		
		if self.largest_army != self._curr_player:
			self.largest_army = find_largest_army(self._curr_player, self.largest_army, self.player_list)



		# if longest road has changed 
		# subtract victory pts from player who lost it
		# add victory pts to player who gained it

		# player 1
		if self._curr_player == 0:
			self.longest_road_length = longest_road(self.road0)
		# player 2
		if self._curr_player == 1:
			self.longest_road_length = longest_road(self.road1)
		# player 3
		if self._curr_player == 2:
			 self.longest_road_length = longest_road(self.road2)
		#player 4
		if self._curr_player == 3:
			self.longest_road_length = longest_road(self.road3)

		if self.longest_road_length > self.longest_road:
			self.longest_road = self.longest_road_length
			if self.longest_road2 == None:
				self.player_list[self._curr_player]._vp += 2
				self.longest_road2 = self._curr_player
			else:
				self.player_list[self._curr_player]._vp += 2
				self.player_list[self.longest_road2]._vp -= 2


		if self.player_list[self._curr_player]._vp >= 10:
			self.mode = Modes.GameOver
		

	def noway(self):
		'''
		reset stuff and go back to action
		'''
		self._value = 0
		self._trade_pack1['number'] = 0
		self._trade_pack2['number'] = 0
		self._trade_pack1['res_type'] = None
		self._trade_pack2['res_type'] = None
		self.send_to = None
		self.mode = Modes.Action

	def yesway(self):
		self.actually_trade(self._curr_player, self.send_to)
		# resetting occurs in actually_trade

	def build_start(self):
		self.mode = Modes.Build

	def build_road(self):
		self.mode = Modes.BuildRoad
		self.build_package['type'] = 'road'

	def build_city(self):
		self.mode = Modes.BuildCity
		self.build_package['type'] = 'city'

	def can_build_city(self):
		player = self.player_list[self._curr_player] # easily access obj
		if not self.has_started():
			return False
		elif player._settlements > 0 and player._stone > 2 and \
			 player._wheat > 1:
			 return True
		else:
			return False

	def can_build_set(self):
		player = self.player_list[self._curr_player] # easily access obj
		if not self.has_started():
			return True
		elif player._brick > 0 and player._wheat > 0 and player._wood > 0 \
			 and player._sheep > 0:
			 return True
		else:
			return False

	def build_settlement(self):
		self.mode = Modes.BuildSettlement
		self.build_package['type'] = 'settlement'

		'''
		Add the following to code that actually builds settlement.
		if not self.has_started():
			self.mode = Modes.BuildRoad
		'''

	def cardmode(self):
		# just move into card mode
		self.mode = Modes.BuildCard
	# called when year of plenty card is used
	# 5 functions for each resource that player 
	# could want, adds 2 of wanted resource to player
	# supply
	def plenty_wood(self):
		self.player_list[self._curr_player]._wood += 2
		self.mode = Modes.Action
	
	def plenty_sheep(self):
		self.player_list[self._curr_player]._sheep += 2
		self.mode = Modes.Action

	def plenty_wheat(self):
		self.player_list[self._curr_player]._wheat += 2
		self.mode = Modes.Action

	def plenty_brick(self):
		self.player_list[self._curr_player]._brick += 2
		self.mode = Modes.Action

	def plenty_stone(self):
		self.player_list[self._curr_player]._stone += 2
		self.mode = Modes.Action

	# called when monopoly card used
	# transfers all of wanted resource 
	# to player that used card
	# need to check parameters input

	def monopoly_wood(self):
		for players in self.player_list:
		# if not the player that used the card
			if self.player_list[players] != self.player_list[self._curr_player]:
				# add the current players resource to player who used it
				self.player_list[self._curr_player].wood += self.player_list[players].wood
				# player that didnt use should have none of the wanted resource
				self.player_list[players].wood = 0
		self.mode = Modes.Action

	# apply same comments from above 
	def monopoly_brick(self):
		for players in self.player_list:
			if self.player_list[players] != self.player_list[self._curr_player]:
				self.player_list[self._curr_player].brick += self.player_list[players].brick
				self.player_list[players].brick = 0
		self.mode = Modes.Action

	# apply same comments from above
	def monopoly_wheat(self):
		for players in self.player_list:
			if self.player_list[players] != self.player_list[self._curr_player]:
				self.player_list[self._curr_player].wheat += self.player_list[players].wheat
				self.player_list[players].wheat = 0
		self.modes = Modes.Action
	# apply same comments from above
	def monopoly_sheep(self):
		for players in self.player_list:
			if self.player_list[players] != self.player_list[self._curr_player]:
				self.player_list[self._curr_player].sheep += self.player_list[players].sheep
				self.player_list[players].sheep = 0
		self.mode = Modes.Action
	# apply same comments from above
	def monopoly_stone(self):
		for players in self.player_list:
			if self.player_list[players] != self.player_list[self._curr_player]:
				self.player_list[self._curr_player].stone += self.player_list[players].stone
				self.player_list[players].stone = 0
		self.mode = Modes.action




	def buy_card(self):

		self.player_list[self._curr_player]._wheat -= 1
		self.player_list[self._curr_player]._stone -= 1
		self.player_list[self._curr_player]._sheep -= 1

		self.player_list[self._curr_player].add_card(self.deck.draw_card())

	def has_knight(self):
		for card in self.player_list[self._curr_player]._cards:
			if card.type == "Knight":
				return True
		return False

	def has_year_plenty(self):
		for card in self.player_list[self._curr_player]._cards:
			if card.type == "Year_of_Plenty":
				return True
		return False

	def has_monopoly(self):
		for card in self.player_list[self._curr_player]._cards:
			if card.type == "Monopoly":
				return True
		return False

	def has_roadbuilder(self):
		for card in self.player_list[self._curr_player]._cards:
			if card.type == "Roadbuilder":
				return True
		return False

	def has_wonder(self):
		for card in self.player_list[self._curr_player]._cards:
			if card.type == "WorldWonder":
				return True
		return False

	def use_knight(self):
		card_list = self.player_list[self._curr_player]._cards
		i = 0
		while card_list[i].type is not "Knight":
			i += 1
			if i is len(card_list):
				i -= 1
				break
		card = card_list[i]
		# apply army size change
		card.use(self.player_list[self._curr_player])
		# put card back in deck
		self.deck.return_to_deck(card)
		# remove from player's hand
		self.player_list[self._curr_player]._cards = card_list[0:i] \
													 + card_list[i+1:-1]
		self.mode = Modes.Action

	def use_monopoly(self):
		card_list = self.player_list[self._curr_player]._cards
		i = 0
		while card_list[i].type is not "Monopoly":
			i += 1
			if i is len(card_list):
				i -= 1
				break
		card = card_list[i]
		# apply army size change
		card.use(self.player_list[self._curr_player])
		# put card back in deck
		self.deck.return_to_deck(card)
		# remove from player's hand
		self.player_list[self._curr_player]._cards = card_list[0:i] \
													 + card_list[i+1:-1]

		self.mode = Modes.Monopoly

	def use_year_plenty(self):
		card_list = self.player_list[self._curr_player]._cards
		i = 0
		while card_list[i].type is not "Year_of_Plenty":
			i += 1
			if i is len(card_list):
				i -= 1
				break
		card = card_list[i]
		# put card back in deck
		self.deck.return_to_deck(card)
		# remove from player's hand
		self.player_list[self._curr_player]._cards = card_list[0:i] \
													 + card_list[i+1:-1]
		self.mode = Modes.Plenty

	def use_roadbuilder(self):
		card_list = self.player_list[self._curr_player]._cards
		i = 0
		while card_list[i].type is not "Roadbuilder":
			i += 1
			if i is len(card_list):
				i -= 1
				break
		card = card_list[i]
		# put card back in deck
		self.deck.return_to_deck(card)
		# remove from player's hand
		self.player_list[self._curr_player]._cards = card_list[0:i] \
													 + card_list[i+1:-1]
		self.mode = Modes.BuildRoad
		self.cardflag = 2											 

	def use_wonder(self):
		card_list = self.player_list[self._curr_player]._cards
		i = 0
		while card_list[i].type is not "WorldWonder":
			i += 1
			if i is len(card_list):
				i -= 1
				break
		card = card_list[i]
		# apply vp change
		self.player_list[self._curr_player]._vp += 1
		# put card back in deck
		self.deck.return_to_deck(card)
		# remove from player's hand
		self.player_list[self._curr_player]._cards = card_list[0:i] \
													 + card_list[i+1:-1]
		self.mode = Modes.Action

	def use_card(self):
		self.mode = Modes.UseCard

	def load_map(self, filename, numbers):
		# create random map
		# @ KELVIN how do the tiles, spaces, etc work? 
		self._network = Graph()
		self._node_to_tile = dict()
		self._node_to_coord = dict()
		self._coord_to_node = dict()

		map_file = open(filename, 'r')
		line = map_file.readline()
		while line.find("NODES START") < 0:
			line = map_file.readline()
			if line == "":
				raise Exception ("expected node definitions")
		
		
		# Move up to the line with the node list

		line = map_file.readline()
		while line.find("NODES END") < 0:
			if line == "":
				raise Exception ("WHERE ARE THE NODES MAN???")
			line = line.rstrip()
			line = line.split(" ") # separate by spaces
			self._network.add_vertex(int(line[0])) # add to graph
			self._node_to_tile[int(line[0])] = [] # list of tiles 
			if line[3] is not 'None':
				self._node_to_tile[int(line[0])].append(line[3])
			if line[4] is not 'None':
				self._node_to_tile[int(line[0])].append(line[4])
			if line[5] is not 'None':
				self._node_to_tile[int(line[0])].append(line[5])
			self._node_to_coord[int(line[0])] = (int(line[1]), int(line[2]))
			self._coord_to_node[(int(line[1]), int(line[2]))] = int(line[0])
			line = map_file.readline()
		'''
		a = list(self._network.vertices())
		a.sort()
		for i in range(0, len(a)):
			print(a[i])
		'''
		
		line = map_file.readline()
		while line.find("EDGES START") < 0:
			line = map_file.readline()
			if line == "":
				raise Exception ("expected edge definitions")
		
		line = map_file.readline()
		# move down to edges
		while line.find("EDGES END") < 0:
			line = line.rstrip()
			line = line.split(' ')
			# print((str(line[0]) + ' , ' + str(line[1])))
			self._network.add_edge((int(line[0]), int(line[1])))
			line = map_file.readline()

			

		
		self.filename = filename
		self.numbers = list(numbers)
		self.tiles, self.resource_dict = \
		print_numbers.print_to_board(numbers, filename, self.screen)
		self.node_contains = {node: None for node in self._network.vertices()}

	def draw(self):
		'''
		Draw this bad boy to the screen 
		'''

		# fill in the background
		self.screen.fill(self.bg_color)

		# draw the game board
		self.screen.blit(self.board, (0,-50))

		numbers = list(self.numbers)
		print_numbers.print_to_board(numbers, self.filename, self.screen)


		# Update and draw the group contents 
		#LayeredUpdates.draw(self, self.screen)

		# draw effects
		#self._effects.draw(self.screen)

		# don't forget roads!
		for road in self.road0:
			pygame.draw.line(self.screen, 0xff2400, 
							 self._node_to_coord[road[0]],
							 self._node_to_coord[road[1]],
							 5)
		for road in self.road1:
			pygame.draw.line(self.screen, 0x8ebbeb, 
							 self._node_to_coord[road[0]],
							 self._node_to_coord[road[1]],
							 5)
		for road in self.road2:
			pygame.draw.line(self.screen, 0x800080	, 
							 self._node_to_coord[road[0]],
							 self._node_to_coord[road[1]],
							 5)

		for road in self.road3:
			pygame.draw.line(self.screen, 0x00ff00, 
							 self._node_to_coord[road[0]],
							 self._node_to_coord[road[1]],
							 5)

		# draw settlements
		for node in self.active_settlements:
			self.active_settlements[node].draw(self.screen)
		# now cities
		for node in self.active_cities:
			self.active_cities[node].draw(self.screen)



		# draw the status bar
		self.draw_bar()

		# Draw the win message if necessary 
		if self.mode == Modes.GameOver:
			win_text = "{} WINS!".format(
				PLAYER_NAME[self._curr_player].upper())

			# Render the text
			win_msg = BIG_FONT.render(
				win_text,
				True,
				FONT_COLOR)
			# change position
			msg_rect = pygame.Rect((0, 0), win_msg.get_size())
			msg_rect.center = (MAP_WIDTH / 2, self.screen.get_height() / 2)

			# draw it
			self.screen.blit(win_msg, msg_rect)

		# update the screen
		pygame.display.flip()

		# map has been drawn
		self.map = True

	def greater_than_zero(self):
		return (self._value > 0)

	def up1(self):
		self._value += 1

	def down1(self):
		self._value -= 1

	def done1(self):
		self._trade_pack1['number'] = self._value
		self._value = 0 # reset value
		self.mode = Modes.ResSel2

	def done2(self):
		self._trade_pack2['number'] = self._value
		self._value = 0 # reset value
		self.mode = Modes.YesNo

	def on_click(self, e):
		"""
		A click event has occurred! Heavily borrows from a2 as well. 
		"""

		node_select = False
		# add any modes where clicks should have no effect
		if (self. mode is Modes.GameOver):
			return 

		if (e.type is pygame.MOUSEBUTTONUP
			and e.button is 1
			and pygame.mouse.get_focused()):

			# Insert code for clicking something that IS NOT IN THE MENU
			# IE NOT BUTTONS here

			# interaction with gui panel:
			# will likely require an if else switch when other click 
			# interactions are added
			# check mode

			# let's do that map interaction now!
			if e.pos[0] < 690:
				# convert coords to node
				node = self.click_to_node(e.pos)
				if node is not None:
					node_select = True

				if node_select:
					# depending on the game mode different things happen here
					if self.mode is Modes.BuildSettlement:
						if self.node_contains[node] is None:
							# create a settlement here
							self.create_settlement(node)

					elif self.mode is Modes.BuildCity:
						if self.node_contains[node] == ('s', self._curr_player):
							self.create_city(node)

					elif self.mode is Modes.BuildRoad:
						self._curr_road1 = node
						self.mode = Modes.RoadInter

					elif self.mode is Modes.RoadInter:
						self._curr_road2 = node
						if not (self._curr_road1, self._curr_road2) in \
						   self.road0 and not \
						   (self._curr_road1, self._curr_road2) in self.road2 \
						   and not (self._curr_road1, self._curr_road2) \
						   in self.road3 and not \
						   (self._curr_road1, self._curr_road2) in self.road1 \
						   and \
							not (self._curr_road2, self._curr_road1) in \
						   self.road0 and not \
						   (self._curr_road2, self._curr_road1) in self.road2 \
						   and not (self._curr_road2, self._curr_road1) \
						   in self.road3 and not \
						   (self._curr_road2, self._curr_road1) in self.road1:

							self.make_road(self._curr_road1, self._curr_road2)
							self._curr_road1, self._curr_road2 = None, None
							if self.has_started():
								self.mode = Modes.Action
							elif self.cardflag > 0:
								self.mode = Modes.BuildRoad
							else:
								self.end_turn()
						else:
							self._curr_road1 = None
							self._curr_road2 = None
							self.mode = Modes.BuildRoad

			else:
				# gui
				if self.mode is Modes.Roll:
					button = self.roll_button
					# then check if we clicked the roll button
					if ((not button.condition or button.condition()) and 
						self.get_button_rect(button).collidepoint(e.pos)):
						button.onClick()
						# change mode
						self.resource_allocation(self._dice)
						self.mode = Modes.RollDisplay

				elif self.mode is Modes.RollDisplay:
					# change mode! 
					self.mode = Modes.Action

				elif self.mode is Modes.Action:
					# Check which button was pressed
					for button in self.buttons:
						# If the button is enabled and has a click function, call
						# the function
						if ((not button.condition or button.condition()) and
							self.get_button_rect(button).collidepoint(e.pos)):
							button.onClick()

				elif self.mode is Modes.Trade:
					for cat in self.tradewith:
						if ((not cat.condition or cat.condition()) and
							self.get_button_rect(cat).collidepoint(e.pos)):
							cat.onClick()

				elif self.mode is Modes.ResSel1:
					for cat in self.resources1:
						if ((not cat.condition or cat.condition()) and
							self.get_button_rect(cat).collidepoint(e.pos)):
							cat.onClick()

				elif self.mode is Modes.ResSel2:
					for cat in self.resources2:
						if ((not cat.condition or cat.condition()) and
							self.get_button_rect(cat).collidepoint(e.pos)):
							cat.onClick()

				elif self.mode is Modes.ValSel1:
					for cat in self.numbers1:
						if ((not cat.condition or cat.condition()) and
							self.get_button_rect(cat).collidepoint(e.pos)):
							cat.onClick()

				elif self.mode is Modes.ValSel2:
					for cat in self.numbers2:
						if ((not cat.condition or cat.condition()) and
							self.get_button_rect(cat).collidepoint(e.pos)):
							cat.onClick()

				elif self.mode is Modes.YesNo:
					for cat in self.yesno:
						if ((not cat.condition or cat.condition()) and
							self.get_button_rect(cat).collidepoint(e.pos)):
							cat.onClick()

				elif self.mode is Modes.Build:
					for button in self.construction:
						if ((not button.condition or button.condition()) and
							self.get_button_rect(button).collidepoint(e.pos)):
							button.onClick()

				elif self.mode is Modes.BuildCard:
					for button in self.card_choices:
						if ((not button.condition or button.condition()) and
							self.get_button_rect(button).collidepoint(e.pos)):
							button.onClick()

				elif self.mode is Modes.InvtCheck:
					button = self.ok_button
					# then check if we clicked the okay button
					if ((not button.condition or button.condition()) and 
						self.get_button_rect(button).collidepoint(e.pos)):
						# change mode
						self.mode = Modes.Action

				elif self.mode is Modes.Plenty:
					for button in self.plenty_buttons:
						if ((not button.condition or button.condition()) and 
							self.get_button_rect(button).collidepoint(e.pos)):
							button.onClick()

				elif self.mode is Modes.Monopoly:
					for button in self.monopoly_buttons:
						if ((not button.condition or button.condition()) and
							self.get_button_rect(button).collidepoint(e.pos)):
							button.onClick()

				elif self.mode is Modes.UseCard:
					for button in self.use_cards:
						if ((not button.condition or button.condition()) and
							self.get_button_rect(button).collidepoint(e.pos)):
							button.onClick()

				elif self.mode is Modes.GameOver:
					button = self.game_over
					# then check if we clicked the button
					if ((not button.condition or button.condition()) and 
						self.get_button_rect(button).collidepoint(e.pos)):
						button.onClick()


	def draw_bar(self):
		"""
		Draws the info bar on the right side of the screen. This 
		function is unavoidably quite large, as each panel needs to be
		handled with separate logic.
		"""
		if not self.map: return
		
		line_num = 0
		
		
		#Determine where the mouse is
		mouse_pos = pygame.mouse.get_pos()
		#coords = self.map.tile_coords(mouse_pos)
		
		#draw the background of the bar
		barRect = self.bar_rect
		pygame.draw.rect(self.screen, BAR_COLOR, barRect)
		
		#draw the outline of the bar
		outlineRect = self.bar_rect.copy()
		outlineRect.w -= 1
		outlineRect.h -= 1
		pygame.draw.rect(self.screen, OUTLINE_COLOR, outlineRect, 2)

		# assign string to mode
		mode_string = None
		if self.mode is Modes.Roll:
			mode_string = 'Please Roll'
		elif self.mode is Modes.Action:
			mode_string = 'Choose Action'
		elif self.mode is Modes.RollDisplay:
			mode_string = 'Rolling Dice'
		elif self.mode is Modes.Trade:
			mode_string = 'With Which Player?'
		elif self.mode is Modes.ResSel1:
			mode_string = "From Your Resources?"
		elif self.mode is Modes.ResSel2:
			mode_string = "From Their Resources?"
		elif self.mode is Modes.ValSel1:
			mode_string = "How much " + self._trade_pack1['res_type'] + "?"
		elif self.mode is Modes.ValSel2:
			mode_string = "How much " + self._trade_pack2['res_type'] + "?"
		elif self.mode is Modes.YesNo:
			mode_string = "Sound good " + PLAYER_NAME[self.send_to] + "?"
		elif self.mode is Modes.Build:
			mode_string = "What to build?"
		elif self.mode is Modes.BuildCity \
			 or self.mode is Modes.BuildSettlement:
			mode_string = "Where?"
		elif self.mode is Modes.BuildRoad or self.mode is Modes.RoadInter:
			mode_string = "Build a Road"
		elif self.mode is Modes.BuildCard:
			mode_string = "Buy or use?"
		elif self.mode is Modes.InvtCheck:
			mode_string = "Your Inventory:"
			self.draw_inventory()
		elif self.mode is Modes.UseCard:
			mode_string = "Which Card?"
		elif self.mode is Modes.Plenty:
			mode_string = "What type?"
		elif self.mode is Modes.Monopoly:
			mode_string = "What do you want to control?"
		elif self.mode is Modes.GameOver:
			mode_string = "GAME OVER " + PLAYER_NAME[self._curr_player] + " WINS!"

		# Current turn
		self.draw_bar_title(
			"{}'s turn!".format(PLAYER_NAME[self._curr_player]),
			line_num)
		line_num += 1
		
		# Title for turn info
		self.draw_bar_title("{}".format(mode_string), line_num)
		line_num += 1

		if self.mode is Modes.BuildRoad or self.mode is Modes.RoadInter:
			self.draw_bar_title("From where to where?", line_num)
			line_num += 1

		#divider
		self.draw_bar_div_line(line_num)
		line_num += 1

		if self.mode is Modes.YesNo:
			self.draw_bar_text(PLAYER_NAME[self._curr_player] + " gives up:",
							   line_num)
			line_num += 1
			self.draw_bar_text(str(self._trade_pack1['number']) + " of " +
							   self._trade_pack1['res_type'], line_num)
			line_num += 1
			self.draw_bar_text(PLAYER_NAME[self.send_to] + " gives up:",
							   line_num)
			line_num += 1
			self.draw_bar_text(str(self._trade_pack2['number']) + " of " +
							   self._trade_pack2['res_type'], line_num)

		# current value
		if self.mode is Modes.ValSel1 or self.mode is Modes.ValSel2:
			self.draw_bar_text("Current Value: " + str(self._value), line_num)
			line_num += 1
			self.draw_bar_div_line(line_num)
			line_num += 1


		# button printing
		if self.mode is Modes.Roll:
			self.draw_bar_button(self.roll_button)

		elif self.mode is Modes.RollDisplay:
			self.draw_bar_title("You rolled a: " + str(self._dice), line_num)
			line_num += 1
			self.draw_bar_button(self.ok_button)
		
		elif self.mode is Modes.Action:
			for button in self.buttons:
				self.draw_bar_button(button)

		elif self.mode is Modes.Trade:
			for player in self.tradewith:
				self.draw_bar_button(player)

		elif self.mode is Modes.ResSel1:
			for resource in self.resources1:
				self.draw_bar_button(resource)

		elif self.mode is Modes.ResSel2:
			for resource in self.resources2:
				self.draw_bar_button(resource)

		elif self.mode is Modes.ValSel1:
			for choice in self.numbers1:
				self.draw_bar_button(choice)

		elif self.mode is Modes.ValSel2:
			for choice in self.numbers2:
				self.draw_bar_button(choice)

		elif self.mode is Modes.YesNo:
			for choice in self.yesno:
				self.draw_bar_button(choice)

		elif self.mode is Modes.Build:
			for building in self.construction:
				self.draw_bar_button(building)

		elif self.mode is Modes.BuildCard:
			for button in self.card_choices:
				self.draw_bar_button(button)

		elif self.mode is Modes.InvtCheck:
			self.draw_bar_button(self.ok_button)

		elif self.mode is Modes.UseCard:
			for button in self.use_cards:
				self.draw_bar_button(button)

		elif self.mode is Modes.Plenty:
			for button in self.plenty_buttons:
				self.draw_bar_button(button)

		elif self.mode is Modes.Monopoly:
			for button in self.monopoly_buttons:
				self.draw_bar_button(button)

		elif self.mode is Modes.GameOver:
			self.draw_bar_button(self.game_over)

	# some more drawing functions from a2
	def draw_bar_text(self, text, line_num):
		"""
		Draws text with a specified variable at a specifed line number.
		"""
		line_text = FONT.render(text, True, FONT_COLOR)
		self.screen.blit(
			line_text,
			(self.bar_rect.x + PAD, FONT_SIZE * line_num + PAD))

	def draw_bar_title(self, text, line_num):
		"""
		Draws a title at a specified line number with the specified text.
		"""
		title_text = FONT.render(text, True, FONT_COLOR)
		self.screen.blit(
			title_text,
			(self.bar_rect.centerx - (title_text.get_width()/2),
			FONT_SIZE * line_num + PAD))

	def draw_bar_div_line(self, line_num):
		"""
		Draws a dividing line at a specified line number.
		"""
		y = FONT_SIZE * line_num + FONT_SIZE//2 + PAD
		pygame.draw.line(
			self.screen,
			(50, 50, 50),
			(self.bar_rect.x, y),
			(self.bar_rect.right, y))

	def make_road(self, v1, v2):
		no = self._curr_player
		if no == 0:
			self.road0.append((v1, v2))
		elif no == 1:
			self.road1.append((v1, v2))
		elif no == 2:
			self.road2.append((v1, v2))
		elif no == 3:
			self.road3.append((v1, v2))

		if self.has_started() and self.cardflag is 0:
			player = self.player_list[self._curr_player]
			player._brick -= 1
			player._wood -= 1
		if self.cardflag != 0:
			self.cardflag = 0

	def get_button_rect(self, button):
		"""
		Gets the rectangle bounding a button in screen cordinates.
		"""
		# The y-coordinate is based on its slot number
		y = self.screen.get_height() - BUTTON_HEIGHT * (button.slot + 1)
		return pygame.Rect(self.bar_rect.x,
							y,
							self.bar_rect.width,
							BUTTON_HEIGHT)

	def draw_bar_button(self, button):
		"""
		Renders a button to the bar.
		If the mouse is hovering over the button it is rendered in white,
		else rgb(50, 50, 50).
		"""

		but_rect = self.get_button_rect(button)
		
		# The outline needs a slightly smaller rectangle
		but_out_rect = but_rect
		but_out_rect.width -= 1

		# Determine the button color
		but_color = BAR_COLOR
		
		# The button can't be used
		if button.condition and not button.condition():
			but_color = BUTTON_DISABLED_COLOR
		else:
			# The button can be used
			mouse_pos = pygame.mouse.get_pos()
			if but_rect.collidepoint(mouse_pos):
				# Highlight on mouse over
				but_color = BUTTON_HIGHLIGHT_COLOR
		
		# Draw the button
		pygame.draw.rect(self.screen, but_color, but_rect)
			
		# Draw the outline
		pygame.draw.rect(self.screen, OUTLINE_COLOR, but_out_rect, 2)

		# Draw the text
		but_text = FONT.render(button.text, True, FONT_COLOR)
		self.screen.blit(
			but_text,
			(self.bar_rect.centerx - (but_text.get_width()/2),
			but_rect.y + (BUTTON_HEIGHT//2) - but_text.get_height()//2))

	def draw_inventory(self):
		'''
		draw the current player's inventory on the screen_rect
		'''
		player_obj = self.player_list[self._curr_player] # get player obj
		line_num = 3 # starting point
		self.draw_bar_text("Victory Points: " + str(player_obj.victory_pts), line_num)
		line_num += 1
		self.draw_bar_text("Army Size: " + str(player_obj.armysize), line_num)
		line_num += 1
		self.draw_bar_div_line(line_num)
		line_num += 1
		self.draw_bar_text("Resources: ", line_num)
		line_num += 1
		self.draw_bar_text("Wheat: " + str(player_obj.wheat), line_num)
		line_num += 1
		self.draw_bar_text("Wood: " + str(player_obj.wood), line_num)
		line_num += 1
		self.draw_bar_text("Brick: " + str(player_obj.brick), line_num)
		line_num += 1
		self.draw_bar_text("Stone: " + str(player_obj.stone), line_num)
		line_num += 1
		self.draw_bar_text("Sheep: " + str(player_obj.sheep), line_num)
		line_num += 1
		self.draw_bar_div_line(line_num)
		line_num += 1
		self.draw_bar_text("Construction: ", line_num)
		line_num += 1
		self.draw_bar_text("# Settlements: " + str(player_obj.settlements), line_num)
		line_num += 1
		self.draw_bar_text("# Cities: " + str(player_obj.cities), line_num)
		line_num += 1
		self.draw_bar_div_line(line_num)
		line_num += 1
		self.draw_bar_text("Cards: ", line_num)
		line_num += 1
		self.draw_bar_text("# cards: " + str(len(player_obj._cards)), line_num)

	def click_to_node(self, pos):
		"""
		Takes in position (x, y) tuple and finds the nearest Node 
		Return: node_id (int)
		"""
		x1 = pos[0]
		y1 = pos[1]

		# potential node coordinates:
		man_distance = 10000 # ridiculous starting point
		for (x2, y2) in self._coord_to_node:
			inter_distance = abs(x2-x1) + abs(y2-y1)
			if inter_distance < man_distance:
				(x3, y3) = (x2, y2)
				man_distance = inter_distance
		if man_distance > 25:
			return None
		else:
			return self._coord_to_node[(x3, y3)]


	# class operations happen here
	def actually_trade(self, first_player, second_player):
		''' 
		accepts "frst player" relating to _trade_pack1 and
		"second player" relating to _trade_pack2
		'''
		# what is first player giving up? 
		if self._trade_pack1['res_type'] is 'stone':
			self.player_list[first_player]._stone -= self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'wheat':
			self.player_list[first_player]._wheat -= self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'wood':
			self.player_list[first_player]._wood -= self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'sheep':
			self.player_list[first_player]._sheep -= self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'brick':
			self.player_list[first_player]._brick -= self._trade_pack1['number']

		# and what is the first player gaining? 
		if self._trade_pack2['res_type'] is 'stone':
			self.player_list[first_player]._stone += self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'wheat':
			self.player_list[first_player]._wheat += self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'wood':
			self.player_list[first_player]._wood += self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'sheep':
			self.player_list[first_player]._sheep += self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'brick':
			self.player_list[first_player]._brick += self._trade_pack2['number']

		# what is second player giving up? 
		if self._trade_pack2['res_type'] is 'stone':
			self.player_list[second_player]._stone -= self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'wheat':
			self.player_list[second_player]._wheat -= self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'wood':
			self.player_list[second_player]._wood -= self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'sheep':
			self.player_list[second_player]._sheep -= self._trade_pack2['number']
		elif self._trade_pack2['res_type'] is 'brick':
			self.player_list[second_player]._brick -= self._trade_pack2['number']

		# and what is the second player gaining? 
		if self._trade_pack1['res_type'] is 'stone':
			self.player_list[second_player]._stone += self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'wheat':
			self.player_list[second_player]._wheat += self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'wood':
			self.player_list[second_player]._wood += self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'sheep':
			self.player_list[second_player]._sheep += self._trade_pack1['number']
		elif self._trade_pack1['res_type'] is 'brick':
			self.player_list[second_player]._brick += self._trade_pack1['number']



		# reset stuff
		self._value = 0
		self._trade_pack1['number'] = 0
		self._trade_pack2['number'] = 0
		self._trade_pack1['res_type'] = None
		self._trade_pack2['res_type'] = None
		self.send_to = None
		self.mode = Modes.Action

	def create_settlement(self, node):

		new_settlement = Settlement(self.player_list[self._curr_player], 
					   self._node_to_coord[node])
		self.active_settlements[node] = new_settlement

		self.node_contains[node] = ('s', self._curr_player)
		self.active_nodes.append(node)
		if self.has_started():
			self.mode = Modes.Action
			self.player_list[self._curr_player]._brick -= 1
			self.player_list[self._curr_player]._wood -= 1
			self.player_list[self._curr_player]._sheep -= 1
			self.player_list[self._curr_player]._wheat -= 1
		else:
			self.mode = Modes.BuildRoad



	def create_city(self, node):
		# deactivate settlement
		self.active_settlements[node]._torndown = True

		# buy city
		self.player_list[self._curr_player]._stone -= 3
		self.player_list[self._curr_player]._wheat -= 2
		self.player_list[self._curr_player]._settlements -= 1

		# semantics
		self.active_nodes.append(node)
		self.node_contains[node] = ('c', self._curr_player)
		new_city = City(self.player_list[self._curr_player], 
						self._node_to_coord[node])
		self.active_cities[node] = new_city

		self.mode = Modes.Action

	# allocates resources after the roll of the dice
	def resource_allocation(self, dice_roll):
		# self.node_contains[node] == None if nothing
		#						   == ('s', player #) if settlement
		#						   == ('c', player #) if city

		# self._node_to_tile[node] -> tile1, tile2, tile2
		# tile is a letter if there
		# None if not
		# every node has at least one tile
		#self.tiles is tiles 
		
		# find settlements

		outerloop = 0
		innerloop = 0
		
		# go through every settlement and city
		for node in self.node_contains:
			add = 0
			outerloop += 1

			if self.node_contains[node] is not None:

				# find the letter(s) of this node
				letters = self._node_to_tile[node]
				# if there were letters
				if len(letters) != 0:
					# loop through all of them
					for letter in letters:
						innerloop += 1
						if letter == 'None':
							pass
						else:
							#print(letter)
							# find the resource corresponding to the letter
							resource = self.resource_dict[letter]
							
							# if the number of that tile was = to dice roll
							if self.tiles[letter] == dice_roll:
								if self.node_contains[node] is not None:
									# find the player info
									player_info = self.node_contains[node]
									# find the player who has a node there
									player_num = player_info[1]

									# checks if its a city or settlement
									# and gives proper allocation
									if player_info[0] == 's':
										add = 1
									
									if player_info[0] == 'c':
										add = 2

																		
									# set of checks to determine what resource to give
									# player
									if resource == 'wheat':
										self.player_list[player_num]._wheat += add
									if resource == 'brick':
										self.player_list[player_num]._brick += add
									if resource == 'stone':
										self.player_list[player_num]._stone += add
									if resource == 'wood':
										self.player_list[player_num]._wood += add
									if resource == 'sheep':
										self.player_list[player_num]._sheep += add




