
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
        self.core.float_x = 320
        self.core.float_y = 112 # center of sprite at vertical center of the screen

        self.health = 100

        self.alive = False

        self.phase = 1

        self.type = boss_type # determines behavior

        self.build = {
            1: { 'life': 20, 'sprite_x': 16, 'sprite_y': 0, 'rel_x': -12, 'rel_y': 0, 'destroy': True }, # destructable shield
            2: { 'life': 20, 'sprite_x': 16, 'sprite_y': 0, 'rel_x': -20, 'rel_y': 0, 'destroy': True }, # destructable shield
            3: { 'life': 20, 'sprite_x': 16, 'sprite_y': 0, 'rel_x': -28, 'rel_y': 0, 'destroy': True }, # destructable shield

            4: { 'life': 10, 'sprite_x': 0, 'sprite_y': 32, 'rel_x': -20, 'rel_y': -16, 'destroy': False }, # armor decoration 
            5: { 'life': 10, 'sprite_x': 0, 'sprite_y': 48, 'rel_x': -20, 'rel_y': 16, 'destroy': False }, # armor decoration

        }

        print("I was initialized")



    ''' Update
        Convert precision location to the rect
    '''
    def update(self, enemy_list):
        if self.alive:
            # enemy handler
            for enemy in enemy_list:
                for index in self.build:
                    if enemy.boss_part == index:
                        # Move parts along with boss
                        enemy.x_float = self.core.float_x + self.build[index]['rel_x']
                        enemy.y_float = self.core.float_y + self.build[index]['rel_y']


            # behavior
            if self.phase == 1:
                self.core.float_x -= 0.1
                if self.core.float_x < 250:
                    self.phase = 2


        self.core.update()


    ''' Draw
        Places the image onto the passed screen
    '''
    def draw(self, win):
        if self.alive: # only draw the boss if it's alive
            self.core.draw(win)
