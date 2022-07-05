import pygame
import random
import math

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
        self.gun_angle = 0 # used for bullet firing
        self.type = enemy_type
        self.scale_percent = 100 # used for tracking the scaling size
        self.scale_flag = True # keep track if scaling up or down
        self.angle = 0 # used for trigonometry calculations
        self.speed = 0 # used for targeting calculations
        self.gun_type = 'none' # can't fire
        self.life = 1

        self.load_images(self.type, start_x, start_y)

    def load_images(self, enemy_type, start_x, start_y):
        # empty list to hold all sprite frames; clear it every time this function is called
        self.animation_frames = [] 

        if enemy_type == 0: # Explosion
            self.speed = 0.5
                # Load the sprite sheet
            sprite_sheet = SpriteSheet("assets/Images/enemy_sheet.png")
                # enemy explosion (5 frame animation)
            image = sprite_sheet.get_image(64, 0, 16, 16)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(64, 16, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(64, 32, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(64, 48, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(64, 64, 16, 16)
            self.animation_frames.append(image) 


        if enemy_type > 0 and enemy_type < 5: # Powerup
            self.speed = 0.5
            sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
            image = sprite_sheet.get_image(48, 16 * enemy_type, 16, 16) # 1 frame animation
            self.animation_frames.append(image)

        if enemy_type == 10: # normal enemy ship
            self.speed = 1
            self.life = 2 
            sprite_sheet = SpriteSheet("assets/Images/enemy_sheet.png")
                # enemy sprites (3 frame animation)
            image = sprite_sheet.get_image(0, 0, 16, 16) # (x, y, width, height)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(16, 0, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(32, 0, 16, 16)
            self.animation_frames.append(image) 

        if enemy_type == 11: # red enemy ship
            self.speed = 1
            self.gun_type = 'circle'
            self.life = 3
            sprite_sheet = SpriteSheet("assets/Images/enemy_sheet.png")
                # enemy sprites (3 frame animation)
            image = sprite_sheet.get_image(0, 16, 16, 16) # (x, y, width, height)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(16, 16, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(32, 16, 16, 16)
            self.animation_frames.append(image) 

        if enemy_type == 12: # powerup carrier enemy ship
            self.speed = 1
            self.life = 1
            sprite_sheet = SpriteSheet("assets/Images/enemy_sheet.png")
                # enemy sprites (3 frame animation)
            image = sprite_sheet.get_image(0, 32, 16, 16) # (x, y, width, height)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(16, 32, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(32, 32, 16, 16)
            self.animation_frames.append(image) 

        if enemy_type == 13: # bullet sprayer
            self.gun_type = 'spiral'
            self.speed = 1
            self.life = 10
            self.angle = 90 # centered movement
            sprite_sheet = SpriteSheet("assets/Images/enemy_sheet.png")
                # enemy sprites (3 frame animation)
            image = sprite_sheet.get_image(0, 48, 16, 16) # (x, y, width, height)
            self.animation_frames.append(image)
            image = sprite_sheet.get_image(16, 48, 16, 16)
            self.animation_frames.append(image) 
            image = sprite_sheet.get_image(32, 48, 16, 16)
            self.animation_frames.append(image) 

        # standard variables
        self.image = self.animation_frames[0] # set initial frame
            # Create a mask for collision
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect() 
        self.x_float = float(start_x) # enemy init location (horizontal)
        self.y_float = float(start_y) # enemy init location (vertical)
        self.rect.x = int (self.x_float)
        self.rect.y = int (self.y_float)
        self.frame = 0 # current animation frame
        self.animation_time = 0 # animation delay speed

    def die(self):
        if self.type == 12: # turn into powerup if it's a powerup dropper ship
            powerup = random.randrange(1, 5)
            if powerup < 5:
                self.type = powerup
                self.load_images(self.type, self.x_float, self.y_float)
        else:
            self.type = 0

        self.load_images(self.type, self.rect.x, self.rect.y)


    '''  Update
        Handles animations and enemy behavior
    '''
    def update(self):
        # Animation Frames
        if pygame.time.get_ticks() > self.animation_time + 100:
            self.animation_time = pygame.time.get_ticks()
            self.frame = self.frame + 1

        # Dead
        if self.type == 0: # explodey bits
            self.x_float += self.speed
            if self.frame > 4:
                self.kill()
                return

        # Powerups
        if self.type > 0 and self.type < 5:
            self.x_float -= self.speed;
            self.frame = 0


        # Enemies
        if self.type == 10: # Scooter
            self.x_float -= self.speed # scoot across the screen this fast

            if self.frame > 2: # reset animation loop
                self.frame = 0

        if self.type == 11: # Shooter
            self.x_float -= self.speed

            if pygame.time.get_ticks() > self.shoot_time + 1000:
                self.shoot_time = pygame.time.get_ticks() + random.randrange(0, 1000)
                self.gun_loaded = 1

            if self.frame > 2: # reset animation loop
                self.frame = 0

        if self.type == 12: # Powerup dude (fly like sine wave)
            self.x_float -= self.speed
            calc = math.sin( math.radians(self.angle) )
            self.y_float += calc
            self.angle += 5
            if self.angle > 360:
                self.angle = 0

            self.frame = 1 # neutral
            if calc < -0.2:
                self.frame = 0
            if calc > 0.2:
                self.frame = 2

        if self.type == 13: # Bullet Sprayer; apply trig to 2 axis
            if self.x_float > 200:
                calc = math.sin( math.radians(self.angle) )
                self.x_float -= math.fabs(calc) # always move left no matter the angle
                self.speed = math.fabs(calc) # update for targeting; this guy is still hard to hit because of weird movements
                self.y_float += (calc * 2)
                self.angle += 2
                if self.angle > 360:
                    self.angle = 0
            else:
                self.speed = 0
                if pygame.time.get_ticks() > self.shoot_time + 1000:
                    self.gun_loaded = 1
                if self.gun_angle > 360:
                    self.shoot_time = pygame.time.get_ticks() + random.randrange(0, 1000)
                    self.gun_angle = 0



            if self.frame > 2: # reset animation loop
                self.frame = 0


        self.image = self.animation_frames[self.frame]

        # Powerups "pulse", so use transform scaling
        if self.type > 0 and self.type < 5:
            width = self.rect.width * (self.scale_percent / 100)
            height = self.rect.height * (self.scale_percent / 100)
            if self.scale_flag == True:
                self.scale_percent += 1
                if self.scale_percent > 100:
                    self.scale_flag = False
            else:
                self.scale_percent -= 1
                if self.scale_percent < 80:
                    self.scale_flag = True
            # Scaling from the original, but will be overwritten next update()
            self.image = pygame.transform.scale(self.image, (width, height) )
            self.scaled_rect = self.image.get_rect(center = self.rect.center)
        else:
            self.scaled_rect = self.rect

        # convert float to integer, don't worry about rounding
        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)


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
        win.blit(self.image, self.scaled_rect)
