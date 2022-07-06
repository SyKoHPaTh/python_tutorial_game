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
    def __init__(self, shrapnel_type, source_rect):
        super().__init__()

        self.type = shrapnel_type   # 1 = ship, 2 = laser, 3 = enemy  

        self.animation_frames = []
        sprite_sheet = SpriteSheet("assets/Images/shrapnel.png")

        for sprite_x in range(0, 40, 8): # start, stop, step
            if self.type == 1: # Metal
                image = sprite_sheet.get_image(sprite_x, 0, 8, 8);
                self.animation_frames.append(image)
            if self.type == 2: # Laser
                image = sprite_sheet.get_image(sprite_x, 8, 8, 8);
                self.animation_frames.append(image)
            if self.type == 3: # Explosion
                image = sprite_sheet.get_image(sprite_x, 16, 8, 8);
                self.animation_frames.append(image)
            if self.type == 4: # Stars
                image = sprite_sheet.get_image(sprite_x, 24, 8, 8);
                self.animation_frames.append(image)


        self.rect = image.get_rect(center = source_rect.center)
        self.x_force = 0
        self.y_force = 0
        self.x_float = float(self.rect.x) # shrapnel init location (rect.x,y read from this after conversions)
        self.y_float = float(self.rect.y)
        self.angle = random.randrange(0, 360)
        self.rotation_speed = random.randrange(-5, 5)
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
            elif self.type == 4:
                self.frame = self.frame # no animation
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

        # Rotation from the original, but will be overwritten next update()
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image, self.angle )
        self.scaled_rect = self.image.get_rect(center = self.rect.center)



    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        win.blit(self.image, self.scaled_rect)