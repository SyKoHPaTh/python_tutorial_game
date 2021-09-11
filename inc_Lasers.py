import pygame
import math

from inc_SpriteSheet import SpriteSheet

''' Lasers

    Handles both the player laser, and the enemy laser

    Ammo type:
        0 = straight shot
        1 = homing shot
        2 = chase shot
        3 = calculated aimed shot
'''
class Lasers(pygame.sprite.Sprite):
    ''' Init
        This function is called automatically when we initialize the Class
    '''
    def __init__(self, init_x, init_y, enemy_list, ammo_type, player_laser):
        super().__init__()

        self.frames = []

        sprite_sheet = SpriteSheet("assets/Images/sprite_sheet.png")
            # enemy bullet (red)
        image = sprite_sheet.get_image(48, 16, 16, 16);
        self.frames.append(image) # Frame 0 = Enemy
            # player bullet (blue)
        image = sprite_sheet.get_image(48, 0, 16, 16);
        self.frames.append(image) # Frame 1 = player

        self.mask = pygame.mask.from_surface(image) # create a mask for collision (same for both lasers)

        self.rect = image.get_rect() 
        self.player_laser = player_laser # type of bullet (True = player, False = enemy)

        self.ammo = ammo_type

        # This is used to store the targeted enemy sprite
        self.enemy_target = False

        # Set the laser starting position to the x,y values we were passed
        self.x_float = init_x
        self.y_float = init_y
        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)

        # These are used for math functions
        self.x_force = 0 # affects force applied on x value
        self.y_force = 0 # force on y value
        self.angle = 0 # angle of the laser
        self.speed = 4 # speed of the laser

        # Call special functions
        if self.ammo == 0: # "Straight"
            self.x_force = self.speed
            self.y_force = 0
        elif self.ammo == 1: # "Homing"
            self.enemy_target = enemy_list
        elif self.ammo == 2: # "Chase"
            self.enemy_target = enemy_list
        elif self.ammo == 3: # "Targeted"
            self.calculate_target(enemy_list)

    '''  Update
        Handles animations and gun timing
    '''
    def update(self):
        # Move the laser

        if self.ammo == 0: # This is the "standard" linear way
            if self.player_laser == True: # player
                self.rect.x += self.speed
            else: # enemy
                self.rect.x -= 2

        elif self.ammo == 1: # Homing Shot
            # If there is an enemy...
            list_size = len( self.enemy_target )
            if list_size > 0:
                for enemy in self.enemy_target:
                    # Just "target" the first one!
                    target_x = enemy.rect.x
                    target_y = enemy.rect.y
                    break

                if self.rect.x < target_x: self.rect.x += self.speed / 2
                if self.rect.x > target_x: self.rect.x -= self.speed / 2
                if self.rect.y < target_y: self.rect.y += self.speed / 2
                if self.rect.y > target_y: self.rect.y -= self.speed / 2

            else:
                self.rect.x += self.speed

        elif self.ammo == 2:
            # If there is an enemy...
            list_size = len( self.enemy_target )
            if list_size > 0:
                for enemy in self.enemy_target:
                    # Just "target" the first one!
                    target_x = enemy.rect.x
                    target_y = enemy.rect.y
                    break

                if self.rect.x < target_x: self.x_force += self.speed / 10
                if self.rect.x > target_x: self.x_force -= self.speed / 10
                if self.rect.y < target_y: self.y_force += self.speed / 10
                if self.rect.y > target_y: self.y_force -= self.speed / 10

                if self.x_force > self.speed: self.x_force = self.speed
                if self.x_force < -self.speed: self.x_force = -self.speed
                if self.y_force > self.speed: self.y_force = self.speed
                if self.y_force < -self.speed: self.y_force = -self.speed
            else:
                self.x_force = self.speed
                self.y_force = 0

            # apply the "force" to our coordinates
            self.x_float += self.x_force
            self.y_float += self.y_force

            # convert float to integer, don't worry about rounding
            self.rect.x = int(self.x_float)
            self.rect.y = int(self.y_float)

            # Calculate the angle to rotate the sprite in the direction of the force
            self.angle = math.atan2( self.y_force, self.x_force )

        elif self.ammo == 3:
            # apply the "force" to our coordinates (make the laser move along the line)
            self.x_float += self.x_force
            self.y_float += self.y_force

            # convert float to integer, don't worry about rounding
            self.rect.x = int(self.x_float)
            self.rect.y = int(self.y_float)


        self.image = self.frames[self.player_laser] # default frame

        # bullet offscreen
        if self.rect.x < -16:
            self.kill()
        if self.rect.x > 320:
            self.kill()

    ''' Draw
        Places the current animation frame image onto the passed screen
    '''
    def draw(self, win):
        angle_degree = -(self.angle * 180/math.pi) # convert radians to degrees
        rotated_image = pygame.transform.rotate(self.image, angle_degree) # rotate the image
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.rect.x, self.rect.y)).center )
        win.blit(rotated_image, new_rect.topleft)

    ''' Calculate Target

        enemy_list      Group of enemy sprites
    '''
    def calculate_target(self, enemy_list):
        # 0 - Check to make sure there is, ya know, actually an enemy out there
        list_size = len( enemy_list )
        if list_size == 0:
            # if no enemy, just set laser along a straight line path
            self.x_force = self.speed
            self.y_force = 0
            return

        # 1 - Find the closest enemy to us
        shortest = 999 # set a "range", in this case we want the whole screen (max range (screen width/height): sqrt(320^2 + 240^2) = 400)
        self.enemy_target = False # references the closest enemy sprite
        for enemy in enemy_list:
            # Calculate the distance
            distance = math.sqrt((enemy.rect.x - self.rect.x)**2 + (enemy.rect.y - self.rect.y)**2) # Pythagorean Theorem

            # If the distance to the enemy is shorter than what we know...
            if distance < shortest:
                # update the shortest distance for comparison
                shortest = distance
                # Sprite groups don't support indexing, so reference sprite directly
                self.enemy_target = enemy

        # 2- Calculate laser angle to closest enemy
        if self.enemy_target != False:
            # Get the "middle" of the enemy instead of top-left
            shortest_x = self.enemy_target.rect.x + (self.enemy_target.rect.width / 2)
            shortest_y = self.enemy_target.rect.y + (self.enemy_target.rect.height / 2)

            # "middle" of the laser
            laser_x = self.rect.x + (self.rect.width / 2)
            laser_y = self.rect.y + (self.rect.height / 2)

            # angle of laser to the enemy's current position
            self.angle = math.atan2( shortest_y - laser_y, shortest_x - laser_x );

            # enemy's angle of travel (using defaults, this is 0)
            shortest_angle = math.atan2( shortest_y - shortest_y, shortest_x - shortest_x - self.enemy_target.speed);

            # apply the angle to the x and y and multiply by speed = velocity, account for the enemy's speed and angle as well (target where they will be = intersection)
            self.x_force = ((math.cos(self.angle)) * self.speed) + (math.cos(shortest_angle) * self.enemy_target.speed)
            self.y_force = ((math.sin(self.angle)) * self.speed) + (math.sin(shortest_angle) * self.enemy_target.speed)

            #print ( "Laser: x,y: ", self.rect.x, ", ", self.rect.y, " | x,y (force):", self.x_force, ", ", self.y_force, " angle:", self.angle, " speed:", self.speed)
            #print ( "Enemy: x,y: ", self.enemy_target.rect.x, ", ", self.enemy_target.rect.y, " | angle:", shortest_angle, " speed:", self.enemy_target.speed)

        else:
            # no enemy in range, just shoot "forward"
            self.x_force = self.speed
            self.y_force = 0            
