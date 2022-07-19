import pygame
import random

from inc_Sprite import Sprite

''' Boss

    Meant as a single-entity comprised of many enemy parts; controlls boss behavior
'''
class Boss(object):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, boss_type):
        super().__init__()

        # This is the boss's vulnerable spot
        self.core = Sprite("assets/Images/boss.png", 16, 16, True) # filename, width, height, collidable
        self.core.float_x = 340
        self.core.float_y = 112 # center of sprite at vertical center of the screen

        self.health = 10

        self.alive = False
        self.invincible = True # default; allow boss to introduce themselves 
        self.aggressive = False # pew pews?
        self.shoot_time = 0
        self.phase_timer = 0

        self.phase = 1

        self.type = boss_type # determines behavior

        self.build = {
            1: { 'life': 20, 'sprite_x': 16, 'sprite_y': 0, 'rel_x': -12, 'rel_y': 0, 'destroy': True }, # destructable shield
            2: { 'life': 20, 'sprite_x': 16, 'sprite_y': 0, 'rel_x': -20, 'rel_y': 0, 'destroy': True }, # destructable shield
            3: { 'life': 20, 'sprite_x': 16, 'sprite_y': 0, 'rel_x': -28, 'rel_y': 0, 'destroy': True }, # destructable shield

            4: { 'life': 10, 'sprite_x': 0, 'sprite_y': 32, 'rel_x': -20, 'rel_y': -16, 'destroy': False }, # armor decoration 
            5: { 'life': 10, 'sprite_x': 0, 'sprite_y': 48, 'rel_x': -20, 'rel_y': 16, 'destroy': False }, # armor decoration

            6: { 'life': 20, 'sprite_x': 0, 'sprite_y': 16, 'rel_x': -12, 'rel_y': -28, 'destroy': False, 'gun_type': 'random' }, # gun
            7: { 'life': 20, 'sprite_x': 0, 'sprite_y': 16, 'rel_x': -12, 'rel_y': 28, 'destroy': False, 'gun_type': 'random'  }, # gun

            8: { 'life': 5, 'sprite_x': 32, 'sprite_y': 32, 'rel_x': -8, 'rel_y': -16, 'destroy': False }, # body
            9: { 'life': 5, 'sprite_x': 32, 'sprite_y': 32, 'rel_x': 8, 'rel_y': -14, 'destroy': False }, # body
            10: { 'life': 5, 'sprite_x': 32, 'sprite_y': 32, 'rel_x': 16, 'rel_y': -8, 'destroy': False }, # body

            11: { 'life': 5, 'sprite_x': 32, 'sprite_y': 32, 'rel_x': -8, 'rel_y': 16, 'destroy': False }, # body
            12: { 'life': 5, 'sprite_x': 32, 'sprite_y': 32, 'rel_x': 8, 'rel_y': 14, 'destroy': False }, # body
            13: { 'life': 5, 'sprite_x': 32, 'sprite_y': 32, 'rel_x': 16, 'rel_y': 8, 'destroy': False }, # body

            14: { 'life': 10, 'sprite_x': 32, 'sprite_y': 0, 'rel_x': 4, 'rel_y': -28, 'destroy': False }, # engine
            15: { 'life': 10, 'sprite_x': 32, 'sprite_y': 0, 'rel_x': 4, 'rel_y': 28, 'destroy': False }, # engine
            16: { 'life': 10, 'sprite_x': 32, 'sprite_y': 0, 'rel_x': 32, 'rel_y': 0, 'destroy': False }, # engine
        }


    ''' Update
        Convert precision location to the rect
    '''
    def update(self, enemy_list, player):
        if self.alive:
            # enemy handler
            for enemy in enemy_list:
                for index in self.build:
                    if enemy.boss_part == index:
                        # Move parts along with boss
                        enemy.x_float = self.core.float_x + self.build[index]['rel_x']
                        enemy.y_float = self.core.float_y + self.build[index]['rel_y']
                        # gun will fire if it's not "destroyed"
                        if self.aggressive and enemy.life > 1:
                            enemy.gun_loaded = 1

            # behavior
            if self.phase == 1: # Enter screen
                self.core.float_x -= 0.1
                if self.core.float_x < 250:
                    self.phase = 2
                    self.invincible = False
                    self.aggressive = True
                    self.phase_timer = pygame.time.get_ticks()
            if self.phase == 2: # move up and down to chase player and pew pew
                if self.core.float_y < player.rect.y:
                    self.core.float_y += 1
                if self.core.float_y > player.rect.y:
                    self.core.float_y -= 1
                if pygame.time.get_ticks() > self.shoot_time + 100:
                    self.shoot_time = pygame.time.get_ticks()
                    self.aggressive = True
                else:
                    self.aggressive = False
                if pygame.time.get_ticks() > self.phase_timer + 10000:
                    self.phase = 3
                    self.aggressive = False
            if self.phase == 3: # Charge to left side of screen
                self.core.float_x -= 4
                if self.core.float_x < 30:
                    self.phase = 4
                    self.phase_timer = pygame.time.get_ticks()
                    self.aggressive = False
            if self.phase == 4: # Return to right side while pew pewing
                self.core.float_x += 1
                if pygame.time.get_ticks() > self.shoot_time + 100:
                    self.shoot_time = pygame.time.get_ticks()
                    self.aggressive = True
                else:
                    self.aggressive = False
                if self.core.float_x > 250:
                    self.phase = 2
                    self.aggressive = True
                    self.phase_timer = pygame.time.get_ticks()



        self.core.update()


    ''' Draw
        Places the image onto the passed screen
    '''
    def draw(self, win):
        if self.alive: # only draw the boss if it's alive
            self.core.draw(win)
