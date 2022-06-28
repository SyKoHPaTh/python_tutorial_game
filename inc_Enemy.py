import pygame
import random

from inc_SpriteSheet import SpriteSheet

''' Enemy
    (sprite group)

    This class handles the badguys which fires lasers

'''

class Enemy(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self):
        super().__init__()

        self.animation_frames = [] # empty list to hold all sprite frames

            # Load the sprite sheet
        sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")

            # enemy sprites (3 frame animation)
        image = sprite_sheet.get_image(0, 16, 16, 16) # (x, y, width, height)
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(16, 16, 16, 16)
        self.animation_frames.append(image) 
        image = sprite_sheet.get_image(32, 16, 16, 16)
        self.animation_frames.append(image) 
            # enemy explosion (4 frame animation)
        image = sprite_sheet.get_image(0, 32, 16, 16)
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(16, 32, 16, 16)
        self.animation_frames.append(image) 
        image = sprite_sheet.get_image(32, 32, 16, 16)
        self.animation_frames.append(image) 
        image = sprite_sheet.get_image(48, 32, 16, 16)
        self.animation_frames.append(image) 

        self.image = self.animation_frames[0] # set initial frame
            # Create a mask for collision (same for both lasers)
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect() 
        self.rect.x = -16 # enemy init location (horizontal) - offscreen
        self.rect.y = -16 # enemy init location (vertical) - offscreen
        self.frame = 1 # current animation frame
        self.animation_time = 0 # animation delay speed
        self.shoot_time = pygame.time.get_ticks() + random.randrange(0, 1000) # delay between firing
        self.gun_loaded = 0  # ready to fire!
        self.alive = True # Flag if we're alive or not


    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
        if pygame.time.get_ticks() > self.shoot_time + 1000:
            self.shoot_time = pygame.time.get_ticks() + random.randrange(0, 1000)
            self.gun_loaded = 1

        # Animation Frames
        if pygame.time.get_ticks() > self.animation_time + 50:
            self.animation_time = pygame.time.get_ticks()
            self.frame = self.frame + 1

        if self.frame > 2 and self.alive == True: # reset animation loop
            self.frame = 0
        elif self.frame > 5 and self.alive == False: # dead :(
            self.kill()

        self.image = self.animation_frames[self.frame]

        self.rect.x -= 1 # scoot across the screen kinda slow

        # Offscreen, remove this sprite
        if self.rect.y < -16: 
            self.kill()
        if self.rect.y > 240:
            self.kill()
        if self.rect.x < -16:
            self.kill()
        if self.rect.x > 320: 
            self.kill()

    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        win.blit(self.image, self.rect)
