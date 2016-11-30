from ResourceCards.cards import *

class Player():

	'''
	Player class that defines stats that every player
	holds. It is used in our game so that it can be 
	passed in as an object to various functions
	so that stats that change can be easily be
	changed by modifing the classes attributes.
	i.e trading(resources change), longestroad(victory pts change)

	'''

	def __init__(self, index, vp = 0, wheat = 0, stone = 0, brick = 0, sheep = 0,
		         wood = 0, settlements = 0, cities = 0, armysize = 0, longestroad = 0):

		# basic stats that player will have
		self._vp = vp
		self._wheat = wheat
		self._wood = wood
		self._brick = brick
		self._stone = stone
		self._sheep = sheep
		self._settlements = settlements
		self._cities = cities
		self._armysize = armysize
		self._longestroad = longestroad
		self._cards = []
		self._index = index
		if type(index) is not int:
			raise Exception("Index is not int")

	@property
	def wheat(self):
		return self._wheat
	@property 
	def wood(self):
		return self._wood
	@property 
	def stone(self):
		return self._stone
	@property 
	def sheep(self):
		return self._sheep
	@property 
	def brick(self):
		return self._brick
	@property 
	def settlements(self):
		return self._settlements
	@property 
	def cities(self):
		return self._cities
	@property 
	def victory_pts(self):
		return self._vp
	@property 
	def armysize(self):
		return self._armysize
	@property
	def longestroad(self):
		return self._longestroad

	def add_card(self, card):
		""" 
		Takes in a card object and adds it to the list of cards
		"""
		self._cards.append(card)

	
	def buy_settlement(self, location):

		'''
		first checks if a player can purchase a settlement
		if player can it makes appropriate changes to players
		victory points and resources.

		'''
		# check if player has the resources
		if self._wood < 1 or self._brick < 1 or self._wheat < 1 or self._sheep < 1:
			raise " Do not have sufficient resources"

		# he does so change his stats
		else:
			self._wood -= 1
			self._brick -= 1
			self._wheat -= 1
			self._sheep -=1 
			self._settlements += 1
			self._vp += 1 

	
	def buy_city(self, settlement):

		'''
		first checks if a player can purchase a city
		if player can it makes appropriate changes to players
		victory points and resources.

		'''

		# check if player has resources
		if self._stone < 3 or self._wheat < 2 or self._settlements is 0:
			raise "Do not have sufficient resources or settlements"
		# player does have resources
		# change stats
		else:
			self._stone -= 3
			self._wheat -= 2
			self._settlements -=1
			self._cities += 1
			self._vp += 1

	# applies changes to player for a purchase of a resource card
	# 1 sheep, 1 stone, 1 wheat are required
	# player will recieve random card
	def buy_resource_card(self):

		# check if player has resources
		if self._stone < 1 or self._wheat < 1 or self._sheep < 1:
			raise "Do not have sufficient resources"
		# player does have resources
		# change stats
		else:
			self._stone -= 1
			self._sheep -= 1
			self._wheat -= 1
			self.cards.append(cards)

	# applies changes to player for a purchase of roads
	# 1 brick and 1 wood are required for a road
	def buy_road(self):

		if self._brick < 1 or self._wood < 1:
			raise "Do not have sufficient resources"
		else:
			self._brick -= 1
			self._wood -= 1

	



