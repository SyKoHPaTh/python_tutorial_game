import pygame

from inc_SpriteSheet import SpriteSheet

''' Lasers

    Handles both the player laser, and the enemy laser
'''
class Lasers(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self):
        super().__init__()

        self.frames = []

        sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
            # player bullet (blue)
        image = sprite_sheet.get_image(48, 0, 16, 16);
        self.frames.append(image) # Frame 1 = player
            # enemy bullet (red)
        image = sprite_sheet.get_image(48, 16, 16, 16);
        self.frames.append(image) # Frame 2 = Enemy

        self.mask = pygame.mask.from_surface(image) # create a mask for collision (same for both lasers)

        self.rect = image.get_rect() 
        self.type = 0 # type of bullet (0 = player, 1 = enemy)


    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
        # Move the laser
        if self.type == 0: # player
            self.rect.x += 8
        else: # enemy
            self.rect.x -= 2

        self.image = self.frames[self.type] # default frame

        # bullet offscreen
        if self.rect.x < -16:
            self.kill()
        if self.rect.x > 320:
            self.kill()

    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        win.blit(self.image, self.rect)
