import pygame
import random
import json

from inc_SpriteSheet import SpriteSheet
from inc_Sprite import Sprite

''' Level

    This replaces the orignal "Terrain" class

    Handles all level effects, such as background, ceiling, ground and everything else

    
    script = dict
    { milliseconds : "COMMAND"}

    * ceiling and ground can come in from offscreen
    * c/g can scroll (different speeds)
    * command: load different sprite for objects (or just kill object and make a new one?)

    * darkness
    * background image
    * stars

    Terrain ceiling/ground:
        There will be collision checking against the player and the enemies

        Image is loaded and then uses a special function "get_image_extend" to place
        a duplicate of the image at the end.  Both images together create one long 
        "sprite" that is 640x40.  This makes scrolling and wrapping easy!

        Once the terrain has scrolled off the screen, it will move to 
        replace the position of the second image (middle of the entire sprite).  
'''
class Level(object):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, level_name):
        super().__init__()

        # Distance is used to go through the script
        self.distance = 0
        self.distance_timer = pygame.time.get_ticks()

        # Load the script [from file]
        # Load Level
        file = 'assets/Levels/' + level_name + '.level'
        with open(file) as readfile:
            self.script = json.load(readfile)
    

        # Flag variables signal when to spawn things outside of the level handler
        self.enemy_flag = False
        self.boss_flag = False

        # Effect: Darkness
        self.darkness_scale = 0 # scaling for the "darkness" screen effect
        self.darkness_timer = 0
        self.darkness_flag = False

        # Effect: Starfield (Scrolling stars)
        self.starfield_active = False
        self.starfield_timer = 0
        self.starfield_flag = False
        self.starfield_speed = 'slow'
        self.starfield_velocity = 0

        # Effect: Background (static image)
        self.background_active = False
        self.background_image = ''
        self.background_loaded = False

        # Effect: Fade 
        self.fade_level = 0  # start at 0 opacity
        self.fade_target = 0  
        self.fade_timer = 0
        self.fade_color = (0,0,0)

        # Effect: Nuke (destroy all enemies)
        self.nuke_flag = False

        # Unique objects
        self.objects = pygame.sprite.Group()


    ''' Increment
        Progresses distance and handles any script events
    '''
    def increment(self):
        # Increment the distance, which is the key of the script dictionary
        if pygame.time.get_ticks() > self.distance_timer + 1:
            self.distance_timer = pygame.time.get_ticks()
            self.distance += 1

        if pygame.time.get_ticks() > self.starfield_timer:
            self.starfield_flag = True
            # the faster stars are, they aren't on screen long, so have shorter timers
            if self.starfield_speed == 'slow':
                self.starfield_timer = pygame.time.get_ticks() + random.randrange(0, 1000)
                self.starfield_velocity = random.randrange(-10, -1) / 10
            elif self.starfield_speed == 'medium':
                self.starfield_timer = pygame.time.get_ticks() + random.randrange(0, 500)
                self.starfield_velocity = random.randrange(-25, -10) / 10
            elif self.starfield_speed == 'fast':
                self.starfield_timer = pygame.time.get_ticks() + random.randrange(0, 100)
                self.starfield_velocity = random.randrange(-100, -25) / 10

        distance_str = str(self.distance)
        if distance_str in self.script:
            self.script_object = self.script[distance_str]
            print( "Script: [", self.distance, "] " , self.script_object)
            # Handle Script Keywords
            if self.script_object['name'] == "ENEMY":
                self.enemy_flag = self.script_object # store details for when the actual enemy spawns
            if self.script_object['name'] == "DARKNESS":
                self.darkness_scale = 300 # percent scale
                self.darkness_timer = pygame.time.get_ticks()
                self.darkness_flag = True
            if self.script_object['name'] == "BRIGHTNESS":
                self.darkness_scale = 100 # percent scale
                self.darkness_timer = pygame.time.get_ticks()
                self.darkness_flag = False
            if self.script_object['name'] == "STARFIELD":
                self.starfield_timer = pygame.time.get_ticks()
                self.starfield_speed = self.script_object['speed']
                if self.script_object['speed'] == 'none':
                    self.starfield_active = False
                else:
                    self.starfield_active = True
            if self.script_object['name'] == "BACKGROUND":
                self.background_active = True
                self.background_file = self.script_object['file']
                self.background_loaded = False
                if self.background_file == 'none':
                    self.background_active = False
            if self.script_object['name'] == "FADE":
                self.fade_target = self.script_object['value']
                self.fade_color = self.script_object['color']
            if self.script_object['name'] == "BOSS":
                self.boss_flag = self.script_object # store boss details
                # stop all repeatable scrolling objects
                for thing in self.objects:
                    thing.scroll_repeat = False
            if self.script_object['name'] == "NUKE":
                self.nuke_flag = True
            if self.script_object['name'] == "OBJECT":
                # filename, width, height, collidable
                object_init = Sprite(self.script_object['file'], self.script_object['width'], self.script_object['height'], self.script_object['collide'])
                object_init.scroll = self.script_object['scroll']
                object_init.scroll_speed = self.script_object['scroll_speed']
                object_init.scroll_repeat = self.script_object['scroll_repeat']
                object_init.float_x = self.script_object['x']
                object_init.float_y = self.script_object['y']
                self.objects.add(object_init)
                if object_init.scroll_repeat: # make a duplicate for scrolling purposes
                    object_init = Sprite(self.script_object['file'], self.script_object['width'], self.script_object['height'], self.script_object['collide'])
                    object_init.scroll = self.script_object['scroll']
                    object_init.scroll_speed = self.script_object['scroll_speed']
                    object_init.scroll_repeat = self.script_object['scroll_repeat']
                    object_init.float_x = self.script_object['x']
                    object_init.float_y = self.script_object['y']
                    if object_init.scroll == 'left':
                        object_init.float_x = self.script_object['x'] + self.script_object['width']
                    if object_init.scroll == 'right':
                        object_init.float_x = self.script_object['x'] - self.script_object['width']
                    if object_init.scroll == 'up':
                        object_init.float_y = self.script_object['y'] + self.script_object['height']
                    if object_init.scroll == 'down':
                        object_init.float_y = self.script_object['y'] - self.script_object['height']
                    self.objects.add(object_init)

            del(self.script[distance_str])



    '''  Update
        Handles animations and timing
    '''
    def update(self):

        if pygame.time.get_ticks() > self.fade_timer + 10:
            self.fade_timer = pygame.time.get_ticks()
            if self.fade_level < self.fade_target:
                self.fade_level += 2
            if self.fade_level > self.fade_target:
                self.fade_level -= 2

        # Object behavior
        for thing in self.objects:
            if thing.scroll == 'left':
                thing.float_x -= thing.scroll_speed
                if thing.rect.y < 0:
                    thing.float_y += (thing.scroll_speed / 10)
                if thing.rect.y + thing.rect.height > 240:
                    thing.float_y -= (thing.scroll_speed / 10)
            if thing.scroll == 'right':
                thing.float_x += thing.scroll_speed
            if thing.scroll == 'up':
                thing.float_y -= thing.scroll_speed
            if thing.scroll == 'down':
                thing.float_y += thing.scroll_speed

            # Offscreen Handling
            if thing.scroll_repeat: # loop the object
                if thing.scroll == 'left' and thing.rect.x + thing.rect.width < 0:
                    thing.float_x += thing.rect.width * 2
                if thing.scroll == 'right' and thing.rect.x > 320:
                    thing.float_x -= thing.rect.width * 2
            else: # eliminate the object
                if thing.scroll == 'left' and thing.rect.x + thing.rect.width < 0:
                    thing.kill()
                if thing.scroll == 'right' and thing.rect.x > 320:
                    thing.kill()

        '''
        # Scroll the terrain
        self.ceiling.float_x -= 0.4
        self.ground.float_x -= 1

        # float_y = 0 # Top of Screen
        if self.ceiling.float_y < 0:
            self.ceiling.float_y += 0.1

        # float_y = 200 # Bottom, minus 40 pixels high
        if self.ground.float_y > 200:
            self.ground.float_y -= 0.1

        # Offscreen
        if self.ceiling.float_x < -320:
            self.ceiling.float_x = 0 # replace the "second" sprite with the first one for "smooth scrolling"
        if self.ground.float_x < -320:
            self.ground.float_x = 0 
        '''

        self.objects.update()


    ''' Draw
        Places all of the level objects
    '''
    def draw(self, win):

        self.objects.draw(win)


