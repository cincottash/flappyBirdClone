from setup import * 
import math
import random
  
def gameLoop(canvas, background, clock, fps):
	gravity = 0.15

	velocity = 0

	acceleration = 0



	done = False

	birdImages = [
	
	pygame.image.load("../assets/sprites/yellowbird-downflap.png"), 
	pygame.image.load("../assets/sprites/yellowbird-midflap.png"), 
	pygame.image.load("../assets/sprites/yellowbird-upflap.png")

	]

	minGap = birdImages[0].get_height() * 2

	birdRects = []


	bottomPipe1 = pygame.image.load("../assets/sprites/pipe-green.png")
	topPipe1 = pygame.transform.rotate(bottomPipe1, 180)

	bottomPipe2 = pygame.image.load("../assets/sprites/pipe-green.png")
	topPipe2 = pygame.transform.rotate(bottomPipe2, 180)

	bottomPipe1Image = bottomPipe1
	topPipe1Image = topPipe1
	bottomPipe2Image = bottomPipe2
	topPipe2Image = topPipe2

	bottomPipe1 = bottomPipe1.get_rect()
	topPipe1 = topPipe1.get_rect()
	bottomPipe2 = bottomPipe2.get_rect()
	topPipe2 = topPipe2.get_rect()

	pipeRectList = []
	pipeRectList.append(bottomPipe1)
	pipeRectList.append(topPipe1)
	pipeRectList.append(bottomPipe2)
	pipeRectList.append(topPipe2)

	for image in birdImages:
		birdRects.append(image.get_rect())

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

	validGap = False

	while(not validGap):

		#INcreasing this value makes them smaller
		bottomPipe1Offset = random.randint(50, 200)
		
		#larger values bring top pipe down
		topPipe1Offset = random.randint(-450, -350)

		bottomPipe2Offset = random.randint(50, 200)
		topPipe2Offset = random.randint(-450, -350)	

		totalGap1 = background.get_height() - bottomPipe1.height + bottomPipe1Offset - topPipe1.height - topPipe1Offset
		totalGap2 = background.get_height() - bottomPipe2.height + bottomPipe2Offset - topPipe2.height - topPipe2Offset
		# print("totalGap1 : {} \n totalGap2: {}\n".format(totalGap1, totalGap2))
		
		if totalGap1 < minGap or totalGap2 < minGap:
			validGap = False
		else:
			validGap = True


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

		bird = birdRects[imageIndex]

		#Stop bird from going off the screen
		if birdY + bird.width > background.get_height():
			# birdY = background.get_height() - bird.height
			# acceleration = 0
			# velocity = 0
			done = True
		elif birdY < 0:
			# birdY = bird.height
			# acceleration = 0
			# velocity = 0
			done = True
		birdImage = birdImages[imageIndex]

		if velocity > 0:
			#rotate between 0 and -45 relative to acceleratation
			#fraction = acceleration/maxAcceleration
			#degrees = fraction * -45
			birdImage = pygame.transform.rotate(birdImage, -45)
		else:
			birdImage = pygame.transform.rotate(birdImage, 25)

		for bird in birdRects:
			bird.x = birdX
			bird.y = birdY

		    	
		canvas.blit(birdImage, (birdX, birdY))

		pipe1X -= 5
		pipe2X -= 5

		#make the second pipe START coming into view as soon as the first pipe STARTS going off screen
		#Reset pipe when it goes offscreen
		if pipe1X + bottomPipe1.width < 0:
			pipe1X = 2 * background.get_width() - topPipe1.width
			offScreen1 = True
		else:
			offScreen1 = False
		#Makes the bottomPipe1 longer or shorter
		if offScreen1:
			validGap = False
			#larger number increases height

			while(not validGap):

				#INcreasing this value makes them smaller
				bottomPipe1Offset = random.randint(50, 200)
				
				#larger values bring top pipe down
				topPipe1Offset = random.randint(-450, -350)

				totalGap1 = background.get_height() - bottomPipe1.height + bottomPipe1Offset - topPipe1.height - topPipe1Offset
				# print("totalGap1 : {} \n totalGap2: {}\n".format(totalGap1, totalGap2))
				
				if totalGap1 < minGap :
					validGap = False
				else:
					validGap = True




		#Reset pipe when it goes offscreen
		if pipe2X + bottomPipe2.width < 0:
			pipe2X = 2 * background.get_width()- topPipe1.width
			offScreen2 = True
		else:
			offScreen2 = False
		#Makes the bottomPipe2 longer or shorter
		if offScreen2:
			validGap = False
			#larger number increases height
			validGap = False
			#larger number increases height

			while(not validGap):

				bottomPipe2Offset = random.randint(50, 200)
				topPipe2Offset = random.randint(-450, -350)	

				#validGap = True

				totalGap2 = background.get_height() - bottomPipe2.height + bottomPipe2Offset - topPipe2.height - topPipe2Offset
				# print("totalGap1 : {} \n totalGap2: {}\n".format(totalGap1, totalGap2))
				
				if totalGap2 < minGap:
					validGap = False
				else:
					validGap = True

		bottomPipe1.x = pipe1X
		bottomPipe1.y = background.get_height()//2 + bottomPipe1Offset

		topPipe1.x = pipe1X
		topPipe1.y = background.get_height()//2 + topPipe1Offset

		bottomPipe2.x = pipe2X
		bottomPipe2.y = background.get_height()//2 + bottomPipe2Offset

		topPipe2.x = pipe2X
		topPipe2.y = background.get_height()//2 + topPipe2Offset


		canvas.blit(bottomPipe1Image, (pipe1X, background.get_height()//2 + bottomPipe1Offset))
		canvas.blit(topPipe1Image, (pipe1X, background.get_height()//2 + topPipe1Offset))

		canvas.blit(bottomPipe2Image, (pipe2X, background.get_height()//2 + bottomPipe2Offset))
		canvas.blit(topPipe2Image, (pipe2X, background.get_height()//2 + topPipe2Offset))

		#Todo: Check for collision with pipes  

		for pipe in pipeRectList:
			if pipe.colliderect(birdRects[imageIndex]):
				done = True


		clock.tick(fps)
		
		pygame.display.update()

		flapping = False

		#Make the bird flap
		if imageIndex == 2:
			imageIndex = 0
		else:
			imageIndex += 1
	gameOverImage = pygame.image.load("../assets/sprites/gameover.png")
	
	
	done = False
	while(not done):
		canvas.blit(background, (0,0))
		canvas.blit(gameOverImage, (background.get_width()//2 - gameOverImage.get_width()//2, background.get_height()//2))
		pygame.display.update()

		for event in pygame.event.get():
		    #Enter will exit the game
		    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
		        done = True
		    elif event.type == pygame.QUIT:
		    	done = True

def main():
	canvas, background, clock, fps = pygameSetup()

	gameLoop(canvas, background, clock, fps)



if __name__ == '__main__':
	main()