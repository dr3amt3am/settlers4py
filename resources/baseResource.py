import pygame, unit, helper, bmpfont
from pygame.sprite import Sprite


SIZE = 50

class BaseResource(Sprite):
	"""
	The basic representation of a resource from which all resource
	types extend. Has a graphical representation and base properties.

	"""

	def __init__(self, tile_x = None, tile_y = None, Number = None **keywords):

		Sprite.__init__(self)

		# Take the keywords off
		self.number = number 

		# set required pygame things.
		self.image = None
		self.rect = pygame.Rect(0, 0, SIZE, SIZE)
		

		# variables for later

		self.brick_up = 0
		self.sheep_up = 0
		self.stone_up = 0
		self.wheat_up = 0
		self.wood_up = 0

		#staticmethod
		def get_resource_at_roll(roll):
			"""
			returns the identified resource at the number

			"""

			for r in baseResource.resources:
				if(roll) == number:
					return r



