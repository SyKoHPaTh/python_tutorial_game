import pygame

''' SpriteSheet
    Class used to grab images out of a sprite sheet

    Loads an image, and cuts out the "sprite" from a sprite sheet
'''
class SpriteSheet(object):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name)

    ''' get_image

        This function converts a loaded image and cuts out the sprite
    '''
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha() # change to convert_alpha() to use alpha as a mask

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        #image.set_colorkey((0, 0, 0)) # remove this, since it is just masking "black"

        return image

    ''' get_image_extend

        A custom function that places 2 of the same image next to each other to create a "long" sprite
        This is a special case for "terrain" only

        (Likely won't need something like this normally)
    '''
    def get_image_extend(self, x, y, width, height):
        image = pygame.Surface([width * 2, height], pygame.SRCALPHA).convert_alpha() # change to convert_alpha() to use alpha as a mask

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.blit(self.sprite_sheet, (width, 0), (x, y, width, height))

        #image.set_colorkey((0, 0, 0))

        return image        