import pygame
import random

from inc_SpriteSheet import SpriteSheet

''' Enemy
    (sprite group)

    This class handles multiple screen entities
        primarily enemies
        also powerups (I know what? just go with it)


    Enemy Types:
        0   red explodey bits
        1   powerup: spread   
        2   powerup: homing
        3   powerup: target
        4   powerup: laser
        5   --placeholder-- maybe a powerup charge +1 for the player powerup selection tree
        10  normal scooter thing that fires one straight pew pew every once in a while

'''

class Enemy(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, enemy_type, start_x, start_y):
        super().__init__()

        self.shoot_time = pygame.time.get_ticks() + random.randrange(0, 1000) # delay between firing
        self.gun_loaded = 0  # ready to fire!
        self.speed = -1 # how "fast" we scoot along the screen (negative = left)
        self.type = enemy_type

        self.load_images(self.type, start_x, start_y)

    def load_images(self, enemy_type, start_x, start_y):
        # empty list to hold all sprite frames; clear it every time this function is called
        self.animation_frames = [] 

        if enemy_type == 0:
                # Load the sprite sheet
            sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
                # enemy explosion (3 frame animation)
            image = sprite_sheet.get_image(0, 32, 16, 16)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(16, 32, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(32, 32, 16, 16)
            self.animation_frames.append(image) 

        if enemy_type > 0 and enemy_type < 5:
            sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
            image = sprite_sheet.get_image(48, 16 * enemy_type, 16, 16) # 1 frame animation
            self.animation_frames.append(image)

        if enemy_type == 10:
            sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
                # enemy sprites (3 frame animation)
            image = sprite_sheet.get_image(0, 16, 16, 16) # (x, y, width, height)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(16, 16, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(32, 16, 16, 16)
            self.animation_frames.append(image) 

        # standard variables
        self.image = self.animation_frames[0] # set initial frame
            # Create a mask for collision
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect() 
        self.rect.x = start_x # enemy init location (horizontal)
        self.rect.y = start_y # enemy init location (vertical)
        self.frame = 0 # current animation frame
        self.animation_time = 0 # animation delay speed

    def die(self):
        self.type = 0
        self.load_images(self.type, self.rect.x, self.rect.y)


    '''  Update
        Handles animations and enemy behavior
    '''
    def update(self):
        # Animation Frames
        if pygame.time.get_ticks() > self.animation_time + 50:
            self.animation_time = pygame.time.get_ticks()
            self.frame = self.frame + 1

        # Dead
        if self.type == 0: # explodey bits
            if self.frame > 2:
                # turn into powerup?
                powerup = random.randrange(1, 10)
                if powerup < 5:
                    print("Powerup type: ", powerup)
                    self.type = powerup
                    self.load_images(self.type, self.rect.x, self.rect.y)
                else:
                    print('ded: ', powerup)
                    self.kill()
                    return

        # Powerups
        if self.type > 0 and self.type < 5:
            self.rect.x -= 1;
            self.frame = 0


        # Enemies
        if self.type == 10: # Scooter
            self.rect.x += self.speed # scoot across the screen this fast

            if pygame.time.get_ticks() > self.shoot_time + 1000:
                self.shoot_time = pygame.time.get_ticks() + random.randrange(0, 1000)
                self.gun_loaded = 1

            if self.frame > 2: # reset animation loop
                self.frame = 0


        self.image = self.animation_frames[self.frame]

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
