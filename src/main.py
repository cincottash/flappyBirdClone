from setup import * 
import math
import random

def gameLoop(canvas, background, clock, fps):
	gravity = 0.2

	velocity = 0

	acceleration = 0

	done = False

	birdImages = [
	
	pygame.image.load("../assets/sprites/yellowbird-downflap.png"), 
	pygame.image.load("../assets/sprites/yellowbird-midflap.png"), 
	pygame.image.load("../assets/sprites/yellowbird-upflap.png")

	]

	bottomPipe = pygame.image.load("../assets/sprites/pipe-green.png")
	#topPipe = pygame.image.load("../assets/sprites/pipe-green.png")
	topPipe = pygame.transform.rotate(bottomPipe, 180)

	imageIndex = 0

	birdX = background.get_width()//8

	birdY = background.get_height()//6

	pipeX = background.get_width() - bottomPipe.get_width()

	maxVelocity = 10
	maxAcceleration = 2.5

	flapping = False

	offScreen = False

	bottomPipeOffset = random.randint(50, 200)
	topPipeOffset = -400

	while(not done):
		canvas.blit(background, (0,0))

		for event in pygame.event.get():
		    #Enter will exit the game
		    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
		        done = True
		    elif event.type == pygame.QUIT:
		    	done = True
		    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
		        acceleration = 0
		        acceleration -= 12 * gravity	
		        flapping = True
		#Briefly ignore gravity whenever we press the space bar so we can get better lift
		if not flapping:
			acceleration += gravity

		velocity += acceleration

		#Keep velocity and acceleration bounded 
		if math.sqrt(velocity**2) > maxVelocity:
			if velocity < 0:
				velocity = -maxVelocity
			else:
				velocity = maxVelocity
		if math.sqrt(acceleration**2) > maxAcceleration:
			if acceleration < 0:
				acceleration = -maxAcceleration
			else:
				acceleration = maxAcceleration

		birdY += velocity

		bird = birdImages[imageIndex]

		#Stop bird from going off the screen
		if birdY + bird.get_height() > background.get_height():
			birdY = background.get_height() - bird.get_height()
			acceleration = 0
			velocity = 0
		elif birdY < 0:
			birdY = bird.get_height()
			acceleration = 0
			velocity = 0

		if velocity > 0:
			bird = pygame.transform.rotate(bird, -45)
		else:
			bird = pygame.transform.rotate(bird, 45)

		    	
		canvas.blit(bird, (birdX, birdY))

		pipeX -= 5

		#Reset pipe when it goes offscreen
		if pipeX + bottomPipe.get_width()< 0:
			pipeX = background.get_width() - bottomPipe.get_width()
			offScreen = True
		else:
			offScreen = False
		#Makes the bottomPipe longer or shorter
		if offScreen:
			#larger number increases height
			bottomPipeOffset = random.randint(50, 200)
			topPipeOffset = random.randint(-400, -250)


		canvas.blit(bottomPipe, (pipeX, background.get_height()//2 + bottomPipeOffset))
		canvas.blit(topPipe, (pipeX, background.get_height()//2 + topPipeOffset))

		#Todo: Check for collision with pipes

		clock.tick(fps)
		
		pygame.display.update()

		flapping = False

		#Make the bird flap
		if imageIndex == 2:
			imageIndex = 0
		else:
			imageIndex += 1
	pygame.quit()
	exit(0)

def main():
	canvas, background, clock, fps = pygameSetup()

	gameLoop(canvas, background, clock, fps)



if __name__ == '__main__':
	main()