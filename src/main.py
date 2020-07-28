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

	bottomPipe1 = pygame.image.load("../assets/sprites/pipe-green.png")
	topPipe1 = pygame.transform.rotate(bottomPipe1, 180)

	bottomPipe2 = pygame.image.load("../assets/sprites/pipe-green.png")
	topPipe2 = pygame.transform.rotate(bottomPipe2, 180)

	imageIndex = 0

	birdX = background.get_width()//8

	birdY = background.get_height()//6

	pipe1X = background.get_width() 
	pipe2X = 2 * background.get_width()

	maxVelocity = 10
	maxAcceleration = 2.5

	flapping = False

	offScreen1 = False
	offScreen2 = False

	bottomPipe1Offset = random.randint(50, 200)
	topPipe1Offset = random.randint(-400, -250)

	bottomPipe2Offset = random.randint(50, 200)
	topPipe2Offset = random.randint(-400, -250)	

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

		pipe1X -= 5
		pipe2X -= 5

		#make the second pipe START coming into view as soon as the first pipe STARTS going off screen
		#Reset pipe when it goes offscreen
		if pipe1X + bottomPipe1.get_width() < 0:
			pipe1X = 2 * background.get_width() - topPipe1.get_width()
			offScreen1 = True
		else:
			offScreen1 = False
		#Makes the bottomPipe1 longer or shorter
		if offScreen1:
			#larger number increases height
			bottomPipe1Offset = random.randint(50, 200)
			topPipe1Offset = random.randint(-450, -350)

		#Reset pipe when it goes offscreen
		if pipe2X + bottomPipe2.get_width() < 0:
			pipe2X = 2 * background.get_width()- topPipe1.get_width()
			offScreen2 = True
		else:
			offScreen2 = False
		#Makes the bottomPipe2 longer or shorter
		if offScreen2:
			#larger number increases height
			bottomPipe2Offset = random.randint(50, 200)
			topPipe2Offset = random.randint(-450, -350)


		canvas.blit(bottomPipe1, (pipe1X, background.get_height()//2 + bottomPipe1Offset))
		canvas.blit(topPipe1, (pipe1X, background.get_height()//2 + topPipe1Offset))

		canvas.blit(bottomPipe2, (pipe2X, background.get_height()//2 + bottomPipe2Offset))
		canvas.blit(topPipe2, (pipe2X, background.get_height()//2 + topPipe2Offset))

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