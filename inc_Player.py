import pygame

from inc_SpriteSheet import SpriteSheet

''' Player

    This class handles the movable spaceship which fires lasers
'''
class Player(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self):
        super().__init__()
        self.animation_frames = []
        sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
            # player sprites
        image = sprite_sheet.get_image(0, 0, 16, 16);
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(16, 0, 16, 16);
        self.animation_frames.append(image) 
        image = sprite_sheet.get_image(32, 0, 16, 16);
        self.animation_frames.append(image) 

        self.image = self.animation_frames[0] # initial frame
            # create a mask for collision (same for both lasers)
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect() 
        self.rect.x = 32 # player init location (horizontal)
        self.rect.y = 120 # player init location (vertical)
        self.frame = 1 # current animation frame
        self.animation_time = 0 # animation delay speed
        self.shoot_time = 0  # delay between firing
        self.gun_loaded = 0  # ready to fire!
        self.alive = True
        self.alive_timer = 0

    ''' Death
        Handles the player dying
    '''
    def death(self):
        if self.alive:
            self.alive = False
            self.alive_timer = pygame.time.get_ticks()

    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
        if pygame.time.get_ticks() > self.shoot_time + 100:
            self.shoot_time = pygame.time.get_ticks()
            self.gun_loaded = 1

        # Animation Frames
        if pygame.time.get_ticks() > self.animation_time + 50:
            self.animation_time = pygame.time.get_ticks()
            self.frame = self.frame + 1

        if self.frame > 2: # reset animation loop
            self.frame = 0

        self.image = self.animation_frames[self.frame]

    '''  Move_
        Movement functions; only move in that direction if it doesn't go offscreen
    '''
    def move_right(self):
        if self.alive:
            if self.rect.x < 304:
                self.rect.x += 2

    def move_left(self):
        if self.alive:
            if self.rect.x > 0:
                self.rect.x -= 2

    def move_up(self):
        if self.alive:
            if self.rect.y > 0:
                self.rect.y -= 2

    def move_down(self):
        if self.alive:
            if self.rect.y < 224:
                self.rect.y += 2

    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        if self.alive:
            win.blit(self.image, self.rect)
