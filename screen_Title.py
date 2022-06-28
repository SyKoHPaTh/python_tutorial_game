import pygame
import time

# ----- Classes -----

''' Title Screen
		Objective
			Show a title screen for a period of time
			Blink "Press any key to Start"

		Returns
			action = "none", "1pstart", "2pstart", "quit"
'''
class Title:
	def __init__(self, configure, gametext):

		self.configure = configure # holds configuration settings
		self.gametext = gametext


	def display(self):

		clock = pygame.time.Clock()

		# Load the graphic for the title screen
		screen_title = pygame.image.load("assets/Images/screen_title.png").convert()

		time = pygame.time.get_ticks()

		# This variable is used to show/hide text on the screen every half second (500ms)
		blink = True
		blink_time = pygame.time.get_ticks()

		status = 'loop'
		while status == 'loop':
			if pygame.time.get_ticks() > blink_time + 500:
				blink_time = pygame.time.get_ticks()
				if blink == True:
					blink = False
				else:
					blink = True

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					status = 'quit'
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						status = 'quit'
					else: # any other key
						status = 'gameplay'

			# Title Image
			self.configure.canvas.blit(screen_title, [0, 0])

			# Show text on screen; Title and Press start

			text = "Tutorial Ship Game"
			self.gametext.text(text, 160, 16, True, True)

			text = "Press any key to Start"

			# This variable determines if the text is shown or not
			if blink == True:
				self.gametext.text(text, 160, 200, True, True) 

			self.configure.display()

			clock.tick(60) #cap FPS

		return status