from cards import *
import random

class Deck():

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

