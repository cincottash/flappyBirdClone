import pygame

def pygameSetup():

	clock = pygame.time.Clock()

	background = pygame.image.load("../assets/sprites/background-day.png")

	canvas = pygame.display.set_mode((background.get_width(), background.get_height()))

	fps = 30

	pygame.init()


	return canvas, background, clock, fps