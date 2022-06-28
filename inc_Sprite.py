import pygame

from inc_SpriteSheet import SpriteSheet

''' Sprite

    Barebones sprite class intended for "dumb" objects (no behavior)
'''
class Sprite(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, image_file, width, height):
        super().__init__()

        sprite_sheet = SpriteSheet(image_file)

            # load the respective image
        sprite_sheet = SpriteSheet(image_file)
        self.image = sprite_sheet.get_image(0, 0, width, height); 
            # create a mask for collision
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect = self.image.get_rect()
        self.float_x = 0 # Used for precise movement
        self.float_y = 0 

    ''' Update
        Convert precision location to the rect
    '''
    def update(self):
        self.rect.x = int(self.float_x)
        self.rect.y = int(self.float_y)

    ''' Draw
        Places the image onto the passed screen
    '''
    def draw(self, win):
        win.blit(self.image, self.rect)
