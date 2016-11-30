import pygame
from pygame.sprite import Sprite

SIZE = 25
SIZE2 = 100

class Road(Sprite, player):

	"""
	This is the road class

	"""

	sprite = pygame.image.load("filename")

	def __init__(self, tile_x = None, tile_y = None, angle = 0 player, **keywords):

		#load the image for a road
		self.image = Road.sprite

		Sprite.__init__(self)


		# get position update

		self.tile_x = tile_x
		self.tile_y = tile_y
		self.angle = angle

		# default attributes

		self.type = "Road"
		self.name = "Road"
		self.rect = pygame.Rect(0,0, SIZE, SIZE2)

		self.image = pygame.transform.rotate(Road.sprite, self._angle)


	def 
