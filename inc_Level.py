import pygame

from inc_SpriteSheet import SpriteSheet
from inc_Sprite import Sprite

''' Level

    This replaces the orignal "Terrain" class

    Handles all level effects, such as background, ceiling, ground and everything else

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


        # Load the sprite sheet, depending on the "type"

        # Unique objects

        # Ceiling and Ground
        self.ceiling = Sprite("assets/Images/ceiling.png", 320, 240)
        self.ceiling.float_y = 0  # override default

        self.ground = Sprite("assets/Images/ground.png", 320, 240)
        self.ground.float_y = 200  # override default


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

        self.ceiling.update()
        self.ground.update()


    ''' Draw
        Places all of the level objects
    '''
    def draw(self, win):

        self.ceiling.draw(win)
        self.ceiling.rect.x += 320
        self.ceiling.draw(win)

        self.ground.draw(win)
        self.ground.rect.x += 320
        self.ground.draw(win)


