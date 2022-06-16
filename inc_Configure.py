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
        self.screen_fit = 'stretch' # stretch, width, height; fit to screen if aspect ratio mismatch
        self.fullscreen = False # pygame.display.toggle_fullscreen()
        self.borderless = False # borderless window
        self.screen_ratio = self.screen_width / self.screen_height # recalculated every time the screen size changes
        self.draw_ratio = self.screen_width / self.screen_height
        self.controller_rumble_id = False

        '''
            label; key value; controller id; key type; button value
            Up
            Down
            Left
            Right
            Fire
            Menu
        '''
        self.control_map = [
                {'label':'Up', 'key':pygame.K_UP, 'id':'keyboard', 'type':'key', 'value':pygame.K_UP},
                {'label':'Down', 'key':pygame.K_DOWN, 'id':'keyboard', 'type':'key', 'value':pygame.K_DOWN},
                {'label':'Left', 'key':pygame.K_LEFT, 'id':'keyboard', 'type':'key', 'value':pygame.K_LEFT},
                {'label':'Right', 'key':pygame.K_RIGHT, 'id':'keyboard', 'type':'key', 'value':pygame.K_RIGHT},
                {'label':'Fire', 'key':pygame.K_SPACE, 'id':'keyboard', 'type':'key', 'value':pygame.K_SPACE},
                {'label':'Menu', 'key':pygame.K_ESCAPE, 'id':'keyboard', 'type':'key', 'value':pygame.K_ESCAPE},
            ]


        self.load()

            # Setup the initial screen (this will be resized)
        self.screen = pygame.display.set_mode([ screen_width, screen_height ])
            # Copy for our screen that we will draw everything to "canvas"
        self.canvas = self.screen.copy()

        self.init_display()

    def init_display(self):
        # Resize the screen from our settings
        flags = 0 # no flag options
        if self.fullscreen == False and self.borderless == True: flags = pygame.NOFRAME  # borderless window
        if self.fullscreen == True and self.borderless == False: flags = pygame.FULLSCREEN # fullscreen
        if self.fullscreen == True and self.borderless == True: flags = pygame.FULLSCREEN | pygame.NOFRAME # borderless and fullscreen (this doesn't make sense, just showing how to combine flags)

        self.screen = pygame.display.set_mode([ self.screen_width, self.screen_height ], flags)

    def display(self):
            # Scale the draw screen to display screen, based on configure settings
        if self.screen_fit == 'stretch': # stretch the canvas to the screen size (distorts if mismatch ratio of 320x240)
            self.screen.blit(pygame.transform.scale(self.canvas, self.screen.get_rect().size), (0, 0) ) 
        elif self.screen_fit == 'width': # fit canvas width to screen
            canvas_height = int( self.screen_width / self.draw_ratio )
            self.screen.blit(pygame.transform.scale(self.canvas, [self.screen_width, canvas_height]), (0, (self.screen_height - canvas_height) // 2 ) ) 
        elif self.screen_fit == 'height':  # fit canvas height to screen
            canvas_width = int( self.screen_height * self.draw_ratio )
            self.screen.blit(pygame.transform.scale(self.canvas, [canvas_width, self.screen_height]), ((self.screen_width - canvas_width) // 2, 0) ) 

            # place the screen on the display via pygame
        pygame.display.flip()


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
        self.screen_fit = file.readline().rstrip('\n')
        self.fullscreen = self.to_bool(file.readline().rstrip('\n'))
        self.borderless = self.to_bool(file.readline().rstrip('\n'))
        self.control_map = [] # clear our control map
        key_label = file.readline().rstrip('\n')
        if key_label == 'KEYMAP:':
            read_keys = True
            while read_keys == True:
                label = file.readline().rstrip('\n')
                if label == 'KEYMAPEND:':
                    read_keys = False
                else:
                    read_dict = {}
                    read_dict.update({'label':label})
                    line = int(file.readline().rstrip('\n'))
                    read_dict.update({'key':line})
                    line = file.readline().rstrip('\n')
                    read_dict.update({'id':line})
                    line = file.readline().rstrip('\n')
                    read_dict.update({'type':line})
                    line = int(file.readline().rstrip('\n'))
                    read_dict.update({'value':line})

                    self.control_map.append(read_dict)
        self.controller_rumble_id = file.readline().rstrip('\n')


        # adjust our calculations!
        self.screen_ratio = self.screen_width / self.screen_height

    def save(self):
        file = open('configure.cfg', 'w')
        file.write( self.format(self.screen_width) )
        file.write( self.format(self.screen_height ) )
        file.write( self.format(self.screen_fit ) )
        file.write( self.format(self.fullscreen ) )
        file.write( self.format(self.borderless ) )
        file.write( "KEYMAP:\n")
        for row in self.control_map:
            file.write( self.format( row['label'] ) )
            file.write( self.format( row['key'] ) )
            file.write( self.format( row['id'] ) )
            file.write( self.format( row['type'] ) )
            file.write( self.format( row['value'] ) )
        file.write( "KEYMAPEND:\n")
        file.write( self.format(self.controller_rumble_id ) )
