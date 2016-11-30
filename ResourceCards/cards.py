"""
classes for different development cards

"""
import random

class Year_of_Plenty:
	""" 
	this card gives the user two resources of their choosing

	"""

	def __init__(self):
		self.type = "Year_of_Plenty"

	def __eq__(self, q):
		return q == self.type

	def __str__(self):
		print("Resource Card: Year of Plenty")

class Monopoly:
	''' 
	This card allows the player to take
	complete control of one resource

	player picks a resource and all other
	players must relinquish all of that resource
	and give it 

	'''

	def __init__(self):

		self.type = "Monopoly"

	def __str__(self):
		return "Resource Card: Monopoly"

		
class Knight:

	def __init__(self):
		self.type = "Knight"

	""" 
	This card contributes to the players army
	and can be used to utilize the robber. 

	"""

	def use(self, player):
		player._armysize += 1

	def __str__(self):
		return "Resource Card: Knight"



class Roadbuilder:

	'''
	this card allows player
	to automatically build 2 roads
	free of charge

	'''

	def __init__(self):
		self.type = "Roadbuilder"

	'''def roads(self):
		team.roads = team.roads + 2
	'''
	def __str__(self):
		return "Resource Card: Road Builder"

class WorldWonder:

	'''
	card grants player one vp

	'''

	def __init__(self):
		self.type = "WorldWonder"

	def vp(self, player):
		player._vp += 1 

	def __str__(self):
		return "Resource Card: World Wonder"


class Deck():

	'''
	class for creating and 
	organizing the deck of cards

	'''

	def __init__(self):
		# 14 knights
		# 2 monopoly cards
		# 2 year of plenty
		# 2 road builders
		# 5 world wonder
		self.cards = [] 

		for i in range(0, 14):
			knight = Knight()
			self.cards.append(knight)

		for i in range (0, 2):
			mono = Monopoly()
			self.cards.append(mono)

		for i in range (0, 2):
			year = Year_of_Plenty()
			self.cards.append(year)

		for i in range (0, 2):
			road = Roadbuilder()
			self.cards.append(road)

		for i in range (0, 5):
			wonder = WorldWonder()
			self.cards.append(wonder)

	def shuffle(self):
		''' shuffle the deck '''
		random.shuffle(self.cards)

	def draw_card(self):
		'''
		draws a card
		'''
		if len(self.cards) is 0:
			raise Exception("Out of cards!")

		a = self.cards.pop()
		return a

	def return_to_deck(self, card):
		''' 
		returns a used card to deck
		reshuffle
		'''
		self.cards.append(card)
		self.shuffle()

