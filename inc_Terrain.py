import pygame

from inc_SpriteSheet import SpriteSheet

''' Terrain

    This handles the "ceiling" and "ground" that will scroll from the right to the left

    There will be collision checking against the player and the enemies

    Image is loaded and then uses a special function "get_image_extend" to place
    a duplicate of the image at the end.  Both images together create one long 
    "sprite" that is 640x40.  This makes scrolling and wrapping easy!

    Once the terrain has scrolled off the screen, it will move to 
    replace the position of the second image (middle of the entire sprite).  
'''
class Terrain(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, land_type):
        super().__init__()

        self.land_type = land_type # This is just a flag to determine which image and location to use

        # Load the sprite sheet, depending on the "type"
        if land_type == 0: # Ceiling
            sprite_sheet = SpriteSheet("assets/Images/ceiling.png")
        else: # Ground
            sprite_sheet = SpriteSheet("assets/Images/ground.png")

            # load the respective image
        self.image = sprite_sheet.get_image_extend(0, 0, 320, 240); 
            # create a mask for collision
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect()
        self.float_x = 0 # Used for precise movement
        if land_type == 0: # Ceiling
            self.float_y = -40 # Vertical
        else: # Ground
            self.float_y = 240 # Vertical

    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
        # Scroll the terrain
        self.float_x -= 0.4

        if self.land_type == 0: # Ceiling
            #self.float_y = 0 # Top of Screen
            if self.float_y < 0:
                self.float_y += 0.1
        else: # Ground
            #self.float_y = 200 # Bottom, minus 40 pixels high
            if self.float_y > 200:
                self.float_y -= 0.1

        # Offscreen
        if self.float_x < -320:
            self.float_x = 0 # replace the "second" sprite with the first one for "smooth scrolling"

        # Apply the (float) values to the rect (int), no rounding needed
        self.rect.x = int(self.float_x)
        self.rect.y = int(self.float_y)


    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        win.blit(self.image, self.rect) # original sprite


