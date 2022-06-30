import pygame

from inc_SpriteSheet import SpriteSheet

''' PlayerHitbox

    This class handles the hitbox which is always on the player's sprite
'''
class PlayerHitbox(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self):
        super().__init__()
        self.animation_frames = []
        sprite_sheet = SpriteSheet("assets/Images/player_ship.png")

            # hitbox "heart", which is the only part of the sprite that can be hit
        image = sprite_sheet.get_image(96, 0, 4, 4) 
        self.animation_frames.append(image)
        image = sprite_sheet.get_image(96, 4, 4, 4)
        self.animation_frames.append(image) 
        image = sprite_sheet.get_image(96, 8, 4, 4)
        self.animation_frames.append(image) 

            # create a mask for collision, based off the "heart"
        self.mask = pygame.mask.from_surface(image) 

        self.rect = image.get_rect()  # note that location will be updated constantly from Player class
        self.frame = 1 # current animation frame
        self.animation_time = 0 # animation delay speed


    '''  Update
        Handles location
    '''
    def update(self, location_rect):

        # Animation Frames
        if pygame.time.get_ticks() > self.animation_time + 50:
            self.animation_time = pygame.time.get_ticks()
            self.frame = self.frame + 1

        # reset animation loop
        if self.frame > 2: 
            self.frame = 0

        self.image = self.animation_frames[self.frame]

        center_rect = self.image.get_rect(center = location_rect.center)


        self.rect.x = center_rect.x
        self.rect.y = center_rect.y + 4 # modify to "feel" like the center of the ship


    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win, invincible_timer):
        if invincible_timer == 0:
            win.blit(self.image, self.rect)
