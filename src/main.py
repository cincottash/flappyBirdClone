from setup import * 
import math

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

	imageIndex = 0
	#Bird always stays in the middle of the screen
	birdX = background.get_width()//2

	#This will be changed
	birdY = background.get_height()//6

	maxVelocity = 10
	maxAcceleration = 2.5

	flapping = False

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
		        acceleration -= 8 * gravity	
		        flapping = True
		if not flapping:
			acceleration += gravity

		velocity += acceleration

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
		    	
		canvas.blit(bird, (birdX, birdY))

		clock.tick(fps)
		
		pygame.display.update()

		flapping = False

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