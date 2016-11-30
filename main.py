import sys, pygame
from gui import GUI
import print_numbers
RESOLUTION = pygame.Rect(0, 0, 911, 600)
BG_COLOR = (0, 0, 0)

# initialize
pygame.mixer.pre_init(22050, -16, 2, 512) # buffer
pygame.init()
pygame.display.set_caption("Settlers of Catan!")
main_gui = GUI(RESOLUTION, BG_COLOR)
clock = pygame.time.Clock()
argv = sys.argv[1:]
numbers = print_numbers.random_order()

# default is random, otherwise override with whatever filename given
level = "random"
if len(argv) > 0:
	level = argv[0]
	main_gui.load_map("maps/" + level + ".lvl", numbers)
else:
	main_gui.load_map("maps/default.lvl", numbers)

# game loop
while True:
	for event in pygame.event.get():
		if event.type is pygame.QUIT:
			pygame.display.quit()
			sys.exit()
		# end if q is pressed
		elif (event.type is pygame.KEYDOWN and (event.key is pygame.K_q 
			or event.key is pygame.K_ESCAPE)):
			pygame.display.quit()
			sys.exit()
		# end turn if e is pressed
		elif (event.type is pygame.KEYDOWN and (event.key is pygame.K_e)):
			main_gui.end_turn()
		# respond to clicks
		elif event.type is pygame.MOUSEBUTTONUP:
			main_gui.on_click(event)
	main_gui.update()
	main_gui.draw()
	clock.tick(60)
	