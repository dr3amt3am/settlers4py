import pygame
from pygame.sprite import Sprite 

SIZE = 25
	
class City(Sprite):

	"""
	This is the City class

	"""

	def __init__(self, player, pos):

		Sprite.__init__(self)

		self.sprite = pygame.image.load("imgs/cit"+str(player._index)+".jpg")

		# default stats
		self.type = "City"
		self.rect = pygame.Rect(0, 0, SIZE, SIZE)
		self.x = int(pos[0] - 13)
		self.y = int(pos[1] - 13)
		self._pos = (self.x, self.y)


		# add appropriate stats to player
		player._cities += 1
		player._vp += 1

	# draw to screen
	def draw(self, screen):

		screen.blit(self.sprite, self._pos)
		