import pygame
from pygame.sprite import sprite
from resources.baseResource import BaseResource

class Sheep(BaseResource):

	"""
	This is the Sheep resource
	increases Sheep resource by 1 if 
	corresponding # is rolled

	"""

	spirte = pygame.image.load("insert file name here")

	def __init__(self, **keywords):

		#load from base class
		super().__init__(**keywords)
		self.image = Sheep.sprite

		# resource specific

		self.type = "Sheep"
		self.resource_change = 1
		self.resource_change2 = 2
		self.name = "Sheep"

	