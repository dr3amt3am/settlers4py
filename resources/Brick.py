import pygame
from pygame.sprite import sprite
from resources.baseResource import BaseResource

class Brick(BaseResource):

	"""
	This is the Brick resource
	increases Brick resource by 1 if 
	corresponding # is rolled

	"""

	sprite = pygame.image.load("insert file name here")

	def __init__(self, **keywords):

		#load from base class
		super().__init__(**keywords)
		self.image = Brick.sprite

		# resource specific

		self.type = "Brick"
		self.resource_change = 1
		self.resource_change2 = 2
		self.name = "Brick"
