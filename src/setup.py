import pygame
from globals import *
def pygameSetup():

	clock = pygame.time.Clock()

	background = pygame.image.load("../assets/sprites/background-day.png")

	canvas = pygame.display.set_mode((background.get_width(), background.get_height()))

	fps = 30

	birdImages = [
	
	pygame.image.load("../assets/sprites/yellowbird-downflap.png"), 
	pygame.image.load("../assets/sprites/yellowbird-midflap.png"), 
	pygame.image.load("../assets/sprites/yellowbird-upflap.png")

	]

	birdRects = []
	for image in birdImages:
		birdRects.append(image.get_rect())

	pygame.init()


	return canvas, background, clock, fps, birdImages, birdRects