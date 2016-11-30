import pygame
from pygame.sprite import Sprite 

SIZE = 25
	
class Settlement(Sprite):
	
	"""
	This is the settlement class

	"""	
	def __init__(self, player, pos):

		self.sprite = pygame.image.load("imgs/set"+str(player._index)+".jpg")
		Sprite.__init__(self)

		# default stats
		self.type = "Settlement"
		self.rect = pygame.Rect(0, 0, SIZE, SIZE)
		player._settlements += 1
		self.x = int(pos[0] - 13)
		self.y = int(pos[1] - 13)
		self._pos = (self.x, self.y)
		self._torndown = False

		player._vp += 1

	
	def draw(self, screen):
		if self._torndown:
			# if a city is built over this settlement, do not draw it!
			return
		else:
			screen.blit(self.sprite, self._pos)



	