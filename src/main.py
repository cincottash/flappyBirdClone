from setup import * 
import math
import random
import os
  
def gameLoop():
	canvas, background, clock, fps, birdImages, birdRects = pygameSetup()

	gravity = 0.15

	velocity = 0

	acceleration = 0

	maxVelocity = 8

	maxAcceleration = 2.5

	score = 0

	done = False

	flapping = False

	offScreen1 = False

	offScreen2 = False

	validGap = False

	minGap = birdImages[0].get_height() * 2
	

	numberImages = []
	# for fileName in os.listdir("../assets/numbers/"):
	# 	numberImages.append(pygame.image.load("../assets/numbers/{}".format(fileName)))
	numberImages.append(pygame.image.load("../assets/numbers/0.png"))
	numberImages.append(pygame.image.load("../assets/numbers/1.png"))
	numberImages.append(pygame.image.load("../assets/numbers/2.png"))
	numberImages.append(pygame.image.load("../assets/numbers/3.png"))
	numberImages.append(pygame.image.load("../assets/numbers/4.png"))
	numberImages.append(pygame.image.load("../assets/numbers/5.png"))
	numberImages.append(pygame.image.load("../assets/numbers/6.png"))
	numberImages.append(pygame.image.load("../assets/numbers/7.png"))
	numberImages.append(pygame.image.load("../assets/numbers/8.png"))
	numberImages.append(pygame.image.load("../assets/numbers/9.png"))


	bottomPipe1Image = pygame.image.load("../assets/sprites/pipe-green.png")
	topPipe1Image = pygame.transform.rotate(bottomPipe1Image, 180)

	bottomPipe2Image = bottomPipe1Image
	topPipe2Image = topPipe1Image

	bottomPipe1Rect = bottomPipe1Image.get_rect()
	topPipe1Rect = topPipe1Image.get_rect()
	bottomPipe2Rect = bottomPipe2Image.get_rect()
	topPipe2Rect = topPipe2Image.get_rect()

	pipeRectList = []

	pipeRectList.append(bottomPipe1Rect)
	pipeRectList.append(topPipe1Rect)
	pipeRectList.append(bottomPipe2Rect)
	pipeRectList.append(topPipe2Rect)

	imageIndex = 0

	for bird in birdRects:
		bird.x = background.get_width()//8

		bird.y = background.get_height()//6

	pipe1X = background.get_width() 
	pipe2X = 2 * background.get_width()


	while(not validGap):

		#INcreasing this value makes them smaller
		bottomPipe1Offset = random.randint(50, 200)
		
		#larger values bring top pipe down
		topPipe1Offset = random.randint(-450, -350)

		bottomPipe2Offset = random.randint(50, 200)
		topPipe2Offset = random.randint(-450, -350)	

		totalGap1 = background.get_height() - bottomPipe1Rect.height + bottomPipe1Offset - topPipe1Rect.height - topPipe1Offset
		totalGap2 = background.get_height() - bottomPipe2Rect.height + bottomPipe2Offset - topPipe2Rect.height - topPipe2Offset
		
		if totalGap1 < minGap and totalGap2 < minGap:
			validGap = False
		else:
			validGap = True


	while(not done):

		bird = birdRects[imageIndex]

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

		for bird in birdRects:
			bird.y += velocity

		#Stop bird from going off the screen
		if bird.y + bird.width > background.get_height():
			done = True
		elif bird.y < 0:
			done = True
		birdImage = birdImages[imageIndex]

		if velocity > 0:
			#rotate between 0 and -45 relative to acceleratation
			#fraction = acceleration/maxAcceleration
			#degrees = fraction * -45
			birdImage = pygame.transform.rotate(birdImage, -45)
		else:
			birdImage = pygame.transform.rotate(birdImage, 25)
		    	
		canvas.blit(birdImage, (bird.x, bird.y))

		pipe1X -= 5
		pipe2X -= 5

		#make the second pipe START coming into view as soon as the first pipe STARTS going off screen
		#Reset pipe when it goes offscreen
		if pipe1X + bottomPipe1Rect.width < 0:
			pipe1X = 2 * background.get_width() - topPipe1Rect.width
			offScreen1 = True
			score+=1
		else:
			offScreen1 = False
		#Makes the bottomPipe1 longer or shorter
		if offScreen1:
			validGap = False
			while(not validGap):

				#INcreasing this value makes them smaller
				bottomPipe1Offset = random.randint(50, 200)
				
				#larger values bring top pipe down
				topPipe1Offset = random.randint(-450, -350)

				totalGap1 = background.get_height() - bottomPipe1Rect.height + bottomPipe1Offset - topPipe1Rect.height - topPipe1Offset
				
				if totalGap1 < minGap :
					validGap = False
				else:
					validGap = True

		#Reset pipe when it goes offscreen
		if pipe2X + bottomPipe2Rect.width < 0:
			pipe2X = 2 * background.get_width()- topPipe1Rect.width
			offScreen2 = True
			score+=1
			#print(score)
		else:
			offScreen2 = False
		#Makes the bottomPipe2 longer or shorter
		if offScreen2:
			#larger number increases height
			validGap = False
			#larger number increases height

			while(not validGap):

				bottomPipe2Offset = random.randint(50, 200)
				topPipe2Offset = random.randint(-450, -350)	

				totalGap2 = background.get_height() - bottomPipe2Rect.height + bottomPipe2Offset - topPipe2Rect.height - topPipe2Offset				
				
				if totalGap2 < minGap:
					validGap = False
				else:
					validGap = True

		bottomPipe1Rect.x = pipe1X
		bottomPipe1Rect.y = background.get_height()//2 + bottomPipe1Offset

		topPipe1Rect.x = pipe1X
		topPipe1Rect.y = background.get_height()//2 + topPipe1Offset

		bottomPipe2Rect.x = pipe2X
		bottomPipe2Rect.y = background.get_height()//2 + bottomPipe2Offset

		topPipe2Rect.x = pipe2X
		topPipe2Rect.y = background.get_height()//2 + topPipe2Offset

		for pipe in pipeRectList:
			if pipe.colliderect(birdRects[imageIndex]):
				done = True

		#TODO: Check for score update
		canvas.blit(bottomPipe1Image, (pipe1X, background.get_height()//2 + bottomPipe1Offset))
		canvas.blit(topPipe1Image, (pipe1X, background.get_height()//2 + topPipe1Offset))

		canvas.blit(bottomPipe2Image, (pipe2X, background.get_height()//2 + bottomPipe2Offset))
		canvas.blit(topPipe2Image, (pipe2X, background.get_height()//2 + topPipe2Offset))

		scoreString = str(score)
		offset = 0

		for digit in scoreString:
			canvas.blit(numberImages[int(digit)], (background.get_width()//10 + offset, background.get_height()//10))
			offset += 1.1 * numberImages[int(digit)].get_width()


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
	gameLoop()


if __name__ == '__main__':
	main()