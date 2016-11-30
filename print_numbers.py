import random
import pygame

# shuffles the list of needed numbers 
def random_order():

	# numbers that are required every game
	numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
	random.shuffle(numbers)
	return numbers

# prints numbers to board and returns dictionary 
# of numbers that are keyed by letters

def print_to_board(numbers, filename, screen):

	'''

	This function reads in the coordinates from a textfile
	to determine where each number should be placed on the board and 
	draws said number to resource tile on the board. 
	two dictionaries are made here to store number and the resource
	it is placed on which is keyed by a letter.

	'''

	# read tile coordinates off of textfile
	# this code is largely modifified from 
	# assignment 2 code
	map_file = open(filename, 'r')
	line = map_file.readline()
	while line.find("RESOURCES START") < 0:
		line = map_file.readline()
		if line == "":
			raise Exception ("Expected resource definitions")
	line = map_file.readline()
	i = 0
	tiles = dict()
	resources = dict()


	while line.find("RESOURCES END") < 0:
		# base string manipulation
		line = line.rstrip()
		line = line.split(' ')
		# find the coordinates for the image
		xcor = int(line[0])
		ycor = int(line[1])
		# remove the used number from list
		number = numbers.pop()

		# determines what number it is
		# and loads the appropriate image
		if number == 2:
			two = pygame.image.load('imgs/2.jpg')
			screen.blit(two, (xcor, ycor))

		if number == 3:
			three = pygame.image.load('imgs/3.jpg')
			screen.blit(three, (xcor, ycor))

		if number == 4:
			four = pygame.image.load('imgs/4.jpg')
			screen.blit(four, (xcor, ycor))

		if number == 5:
			five = pygame.image.load('imgs/5.jpg')
			screen.blit(five, (xcor, ycor))

		if number == 6:
			six = pygame.image.load('imgs/6.jpg')
			screen.blit(six, (xcor, ycor))

		if number == 8:
			eight = pygame.image.load('imgs/8.jpg')
			screen.blit(eight, (xcor, ycor))

		if number == 9:
			nine = pygame.image.load('imgs/9.jpg')
			screen.blit(nine, (xcor, ycor))

		if number == 10:
			ten = pygame.image.load('imgs/10.jpg')
			screen.blit(ten, (xcor, ycor))

		if number == 11:
			eleven = pygame.image.load('imgs/11.jpg')
			screen.blit(eleven, (xcor, ycor))

		if number == 12:
			twelve = pygame.image.load('imgs/12.jpg')
			screen.blit(twelve, (xcor, ycor))

		# assigns number and letter for a tile
		if i == 0:
			tiles['P'] = number
			resources['P'] = 'wood' 
		if i == 1:
			tiles['Q'] = number
			resources['Q'] = 'sheep'
		if i == 2:
			tiles['R'] = number 
			resources['R'] = 'wheat'
		if i == 3:
			tiles['O'] = number
			resources['O'] = 'brick'
		if i == 4:
			tiles['N'] = number
			resources['N'] = 'stone'
		if i == 5: 
			tiles['M'] = number
			resources['M'] = 'brick'
		if i == 6:
			tiles['L'] = number
			resources['L'] = 'sheep'
		if i == 7:
			tiles['H'] = number 
			resources['H'] = 'wood'
		if i == 8:
			tiles['I'] = number
			resources['I'] = 'wheat'
		if i == 9:
			tiles['J'] = number
			resources['J'] = 'wood'
		if i == 10:
			tiles['K'] = number
			resources['K'] = 'wheat'
		if i == 11:
			tiles['G'] = number
			resources['G'] = 'brick'
		if i == 12:
			tiles['F'] = number
			resources['F'] = 'sheep'
		if i == 13:
			tiles['E'] = number
			resources['E'] = 'sheep'
		if i == 14:
			tiles['D'] = number
			resources['D'] = 'stone'
		if i == 15:
			tiles['A'] = number
			resources['A'] = 'stone'
		if i == 16:
			tiles['B'] = number
			resources['B'] = 'wheat'
		if i == 17:
			tiles['C'] = number
			resources['C'] = 'wood'

		i += 1
		line = map_file.readline()

	return tiles, resources 
