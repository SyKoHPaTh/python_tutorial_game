import pygame
import math
import random

from os.path import exists

# ----- Import from other files ----

# ----- Classes -----
''' Configure
    Handles all Configuration stuff

    Most of this is used for file save/load
'''

class Configure():

    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_mode = 'width' # stretch, width, height; fit to screen if aspect ratio mismatch
        self.fullscreen = False # pygame.display.toggle_fullscreen()
        self.borderless = False # borderless window
        self.screen_ratio = self.screen_width / self.screen_height # recalculated every time the screen size changes
        self.draw_ratio = self.screen_width / self.screen_height

        self.load()

            # Setup the initial screen (this will be resized)
        self.screen = pygame.display.set_mode([ screen_width, screen_height ])
            # Copy for our screen that we will draw everything to "canvas"
        self.canvas = self.screen.copy()

            # Resize the screen from our settings
        flags = 0 # no flag options
        if self.fullscreen == False and self.borderless == True: flags = pygame.NOFRAME  # borderless window
        if self.fullscreen == True and self.borderless == False: flags = pygame.FULLSCREEN # fullscreen
        if self.fullscreen == True and self.borderless == True: flags = pygame.FULLSCREEN | pygame.NOFRAME # borderless and fullscreen (this doesn't make sense, just showing how to combine flags)

        self.screen = pygame.display.set_mode([ self.screen_width, self.screen_height ], flags)

    def display(self):
            # Scale the draw screen to display screen, based on configure settings
        if self.screen_mode == 'stretch': # stretch the canvas to the screen size (distorts if mismatch ratio of 320x240)
            self.screen.blit(pygame.transform.scale(self.canvas, screen.get_rect().size), (0, 0) ) 
        elif self.screen_mode == 'width': # fit canvas width to screen
            canvas_height = int( self.screen_width / self.draw_ratio )
            self.screen.blit(pygame.transform.scale(self.canvas, [self.screen_width, canvas_height]), (0, (self.screen_height - canvas_height) // 2 ) ) 
        elif self.screen_mode == 'height':  # fit canvas height to screen
            canvas_width = int( self.screen_height * self.draw_ratio )
            self.screen.blit(pygame.transform.scale(self.canvas, [canvas_width, self.screen_height]), ((self.screen_width - canvas_width) // 2, 0) ) 

            # place the screen on the display via pygame
        pygame.display.flip()


    def video(self):
        # Video options
        display_info = pygame.display.Info()
        print("Display Info:", display_info)

        fullscreen_modes = pygame.display.list_modes()
        print("Display Modes:", fullscreen_modes)

    def format(self, field):
        return (f'{field}\n')

    def to_bool(self, field):
        if field == 'True':
            return True
        elif field == 'False':
            return False
        else:
            return ValueError # Error flag that doesn't return a type 

    def load(self):
        # check if file exists, if not, create a default
        if not exists('configure.cfg'):
            self.save() # this will save with current default settings

        file = open('configure.cfg', 'r')
        self.screen_width = int(file.readline().rstrip('\n'))
        self.screen_height = int(file.readline().rstrip('\n'))
        self.screen_mode = file.readline().rstrip('\n')
        self.fullscreen = self.to_bool(file.readline().rstrip('\n'))
        self.borderless = self.to_bool(file.readline().rstrip('\n'))

        # adjust our calculations!
        self.screen_ratio = self.screen_width / self.screen_height


    def save(self):
        file = open('configure.cfg', 'w')
        file.write( self.format(self.screen_width) )
        file.write( self.format(self.screen_height ) )
        file.write( self.format(self.screen_mode ) )
        file.write( self.format(self.fullscreen ) )
        file.write( self.format(self.borderless ) )
