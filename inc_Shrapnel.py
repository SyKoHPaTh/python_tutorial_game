import pygame
import random

from inc_SpriteSheet import SpriteSheet

''' Shrapnel
    Class used to handle all shrapnel
'''
class Shrapnel(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, shrapnel_type, x, y):
        super().__init__()

        self.type = shrapnel_type   # 1 = ship, 2 = laser, 3 = enemy  

        self.animation_frames = []
        sprite_sheet = SpriteSheet("assets/Images/shrapnel.png")

        for sprite_x in range(0, 40, 8): # start, stop, step
            if self.type == 1: # Ship
                image = sprite_sheet.get_image(sprite_x, 0, 8, 8);
                self.animation_frames.append(image)
            if self.type == 2: # Laser
                image = sprite_sheet.get_image(sprite_x, 8, 8, 8);
                self.animation_frames.append(image)
            if self.type == 3: # Enemy
                image = sprite_sheet.get_image(sprite_x, 16, 8, 8);
                self.animation_frames.append(image)


        self.rect = image.get_rect() 
        self.rect.x = x # shrapnel init location (horizontal)
        self.rect.y = y # shrapnel init location (vertical)
        self.x_force = 0
        self.y_force = 0
        self.x_float = x
        self.y_float = y
        self.frame = 0 # current animation frame 
        self.animation_timer = 0 # animation timer
        self.animation_delay = 100 # time between animation frames 



    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
        # Animation Frames
        if pygame.time.get_ticks() > self.animation_timer + self.animation_delay:
            self.animation_timer = pygame.time.get_ticks()
            if self.type == 1:
                self.frame = random.randrange(0, 5) # It is only: 0,1,2,3,4
            else:
                self.frame = self.frame + 1

            if self.frame == 5: # reset animation loop
                self.frame = 0
                if self.type == 2 or self.type == 3: # Laser and Enemy only animate loop once
                    self.kill()

        # Apply force to our floats
        self.x_float += self.x_force
        self.y_float += self.y_force

        # convert our float values to int, and apply to the sprite
        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)

        self.image = self.animation_frames[self.frame]

    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        win.blit(self.image, self.rect)