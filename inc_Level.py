import pygame

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
    def __init__(self):
        super().__init__()

        # Distance is used to go through the script
        self.distance = 0
        self.distance_timer = pygame.time.get_ticks()

        # Load the script [from file]
        self.script = { 
            100: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
            150: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
            200: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
            250: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },

            300: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
            350: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
            400: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
            450: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },

            500: { 'name': "DARKNESS" },
            800: { 'name': "BRIGHTNESS" }, # lol?
        }

        # Flag variables signal when to spawn things outside of the level handler
        self.enemy_flag = False

        self.darkness_scale = 0 # scaling for the "darkness" screen effect
        self.darkness_timer = 0
        self.darkness_flag = False







        # Unique objects -- delete this section (move to increment)
        self.objects = pygame.sprite.Group()

        # Ceiling and Ground
        ceiling = Sprite("assets/Images/ceiling.png", 320, 240, True) # filename, width, height, collidable
        ceiling.float_y = 0  # override default
        self.objects.add(ceiling)

        ground = Sprite("assets/Images/ground.png", 320, 240, True)
        ground.float_y = 200  # override default
        self.objects.add(ground)


    ''' Increment
        Progresses distance and handles any script events
    '''
    def increment(self):
        # Increment the distance, which is the key of the script dictionary
        if pygame.time.get_ticks() > self.distance_timer + 1:
            self.distance_timer = pygame.time.get_ticks()
            self.distance += 1

        if self.distance in self.script:
            self.script_object = self.script[self.distance]
            print( "activated: " , self.script_object['name'] )
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

            del(self.script[self.distance])



    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
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


