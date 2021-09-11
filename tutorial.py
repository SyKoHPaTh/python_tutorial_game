''' Tutorial

    This is a tutorial game!  

    License:  Free for Public/Personal/Commercial Use

    Author: Alex Beck (SyKoHPaTh)

        Shameful Self-Promotion:
            - Youtube   https://www.youtube.com/SyKoHPaTh
            - Discord   https://discord.gg/UeNKDCJ
            - Twitch    https://www.twitch.tv/sykohpath
            - Twitter   https://twitter.com/sykohpath
            - Website   http://www.sykohpath.com    
'''

# ---- Imports ----
import os 
import pygame
import random
import math

# ---- File Includes ----
from inc_Player import Player
from inc_Enemy import Enemy
from inc_Lasers import Lasers
from inc_Terrain import Terrain

# ----- Initialization -----
# set Environment variables; default initial Window Position
x = 100
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create screens for display
    # This is "classic arcade" size screen; big pixels, old school
WIDTH = 320
HEIGHT = 240

    # used for scaling, so we can actually play it on modern size screens
    # Note that "fullscreen" doesn't need this
ratio = 5 

    # Setup the "arcade" size screen
screen = pygame.display.set_mode([ WIDTH, HEIGHT ])
    # Copy for our screen that we will draw everything to
draw_screen = screen.copy()

    # Window icon
icon = pygame.image.load("assets/Images/icon.png")
pygame.display.set_icon(icon)

    # Window mode (scaled up by Ratio)
screen = pygame.display.set_mode([ (WIDTH * ratio), (HEIGHT * ratio) ]) 
    # Fullscreen mode (don't use ratio)
#screen = pygame.display.set_mode([ (WIDTH), (HEIGHT) ], pygame.FULLSCREEN)

# Hide the mouse
pygame.mouse.set_visible(False)
 
# This sets the name of the window
pygame.display.set_caption('Tutorial Spaceship Shooter')
 
# Clock is used to cap framerate
clock = pygame.time.Clock()

# Load static images
background_image = pygame.image.load("assets/Images/background.png").convert()

# Load the font and set the font size
font = pygame.font.Font("assets/Fonts/upheavtt.ttf", 14)

# Load Sound Effect(s) and Music
sfx_player_shoot = pygame.mixer.Sound("assets/Audio/SF1.wav") 
sfx_player_shoot.set_volume(0.5) # change the volume of the sfx, can use for music too
sfx_enemy_die = pygame.mixer.Sound("assets/Audio/SF10.wav") 
#sfx_enemy_die.set_volume(0.1)
# Music
pygame.mixer.music.load( "assets/Audio/93727__zgump__tr-loop-0416.wav" )

# Setup the sprites
player = Player() # player (from the inc_Player.py class)
terrain_ceiling = Terrain(0) # the terrain ceiling
terrain_ground = Terrain(1) # the terrain ground

    # Sprite Groups are used for multiples of the same thing
enemy_list = pygame.sprite.Group() # Group of all enemy sprites
laser_list = pygame.sprite.Group() # Group of all laser sprites

# ----- Functions -----
''' Game Text
        Objective
            Handles the fancy stuff for placing pretty text on the screen
        Parameter
            text    the text we want to display
            x       x location of the text
            y       y location of the text
            centered    do fancy math to place the text centered at x
'''
def game_text(text, x, y, centered):
    if centered == True:
        x = (x - len(text) * 4)
    text_render = font.render(text, True, (255, 255, 255)) # RGB 
    draw_screen.blit(text_render, [x, y])

''' Main Game Loop
    Everything happens here!
'''
def main():
    # startup variables
        # how often enemies appear
    enemy_spawn_timer = pygame.time.get_ticks() + 9000 # extra delay (9seconds)
    player_fire_button = 'UP' # Polling Key State

    # Prepare the sprite groups, make sure they are empty (good to do for new levels)
    enemy_list.empty()
    laser_list.empty()

    player_alive = True # Flag used to keep the game loop going
    score = 0 # Player's score!

    ''' Laser type:
        0   standard 
        1   Homing
        2   Chase
        3   Targeted
    '''
    ammo_type = 3

    # Start the music loop
        # Enable music Loop by passing -1 to "repeat"
    pygame.mixer.music.play( -1 ) # Starts the music

    # Actual game loop
    while player_alive:
        # -- Event handler --
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Close the window
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Escape Key
                    return "quit";

        # Key Polling, handles "key up" and "key down" actions
        key = pygame.key.get_pressed()
        # Player "Fire" button
        if key[pygame.K_SPACE] == True: # pressing button
            if player_fire_button == 'UP':
                player_fire_button = 'PRESSED'

            if player.gun_loaded == 1:
                player.gun_loaded = 0 # disable flag
                sfx_player_shoot.play(); # Play the SFX

                # Initialize a new laser, and add it to the group
                laser = Lasers(player.rect.x, player.rect.y, enemy_list, ammo_type, True)
                laser_list.add(laser)

        elif key[pygame.K_SPACE] == False: # released button
            if player_fire_button == 'DOWN':
                player_fire_button = 'RELEASE'

        if key[pygame.K_LEFT]:
            player.move_left()
        if key[pygame.K_RIGHT]:
            player.move_right()
        if key[pygame.K_UP]:
            player.move_up()
        if key[pygame.K_DOWN]:
            player.move_down()

        # -- Game Logic --
        # Enemies
            # spawn an enemy
        if pygame.time.get_ticks() > enemy_spawn_timer + 1000:
            enemy_spawn_timer = pygame.time.get_ticks()
            enemy = Enemy()
            enemy.rect.x = 320 # place offscreen
            enemy.rect.y = random.randrange(40, 184) # account for the terrain
            enemy_list.add(enemy)
            # Enemy fire laser
        for enemy_ship in enemy_list:
            if enemy_ship.gun_loaded == 1:
                enemy_ship.gun_loaded = 0
                # Initialize a new laser, and add it to the group
                laser = Lasers(enemy_ship.rect.x, enemy_ship.rect.y, False, 0, False)
                laser_list.add(laser)

        # Hit detection
            # Player crash into terrain
            if pygame.sprite.collide_mask(player, terrain_ceiling) or pygame.sprite.collide_mask(player, terrain_ground):
                player_alive = False # Break the game loop flag = game over

            # Lasers
            for laser in laser_list:
                if laser.player_laser == True: # Player laser hit enemy
                    enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_list, False, pygame.sprite.collide_mask)
                    for enemy in enemy_hit_list:
                        if enemy.alive:
                            enemy.alive = False
                            score += 100
                            sfx_enemy_die.play(); # sfx
                            laser.kill()
                if laser.player_laser == False: # Enemy Laser hits Player
                    if pygame.sprite.collide_mask(laser, player):
                        player_alive = False # Break the game loop flag = game over
                # Laser hits terrain                        
                if pygame.sprite.collide_mask(laser, terrain_ceiling) or pygame.sprite.collide_mask(laser, terrain_ground):
                    laser.kill()

        # -- Sprite and Screen --
            # Call "update" for sprites
        player.update()
        terrain_ceiling.update()
        terrain_ground.update()
            # "update" the sprite groups
        enemy_list.update()
        laser_list.update()

        # Screen Update
            # Draw the background
        draw_screen.blit(background_image, [0, 0])
            # Draw the sprites
                # Note that these are drawn in the order they are called (overlap!)
        enemy_list.draw(draw_screen)
        for laser in laser_list:
            laser.draw(draw_screen) # this overrides the group draw function
        player.draw(draw_screen)
        terrain_ceiling.draw(draw_screen)
        terrain_ground.draw(draw_screen)

#======== This section completely optional ========== Trigonometry is fun!
        if ammo_type == 3: # Targeting laser
            # Check to make sure there is, ya know, actually an enemy out there
            list_size = len( enemy_list )
            if list_size > 0:
                # find the closest enemy to us
                closest = 999 # set a "range", in this case we want the whole screen (max range (screen width/height): sqrt(320^2 + 240^2) = 400)
                closest_x = 0
                closest_y = 0
                for enemy in enemy_list:
                        # Set start/end points to the middle of the sprites
                    start_x = player.rect.x + (player.rect.width / 2)
                    start_y = player.rect.y + (player.rect.height / 2)
                    end_x = enemy.rect.x + (enemy.rect.width / 2)
                    end_y = enemy.rect.y + (enemy.rect.height / 2)

                    # get the distance
                    distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2 ) # Pythagorean Theorem

                    # calculate the angle to the enemy from the spaceship
                    angle = math.atan2( end_y - start_y, end_x - start_x );

                    # Draw a grey line from spaceship to enemy (ez way to do it!)
                    pygame.draw.line(draw_screen, (55, 55, 55), (start_x, start_y), (end_x, end_y) )

                    # Draw Green "points" along the line (calculated way to do it!)
                    b = 0
                    speed = distance / 10
                    f = start_x
                    g = start_y
                    while b < distance:
                        b += speed
                        f = f + (math.cos(angle) * speed);
                        g = g + (math.sin(angle) * speed);
                        pygame.draw.line(draw_screen, (0, 255, 0), [f, g], [f, g] )

                    # Check if this is the closest distance (used for 'red line' below, outside of loop)
                    if distance < closest:
                        closest = distance
                        # Just get the enemy location
                        closest_x = enemy.rect.x
                        closest_y = enemy.rect.y

                # Draw a red line pointing to the closest enemy
                if closest_x != 0 and closest_y != 0:
                    angle = math.atan2( closest_y - player.rect.y, closest_x - player.rect.x );

                # draw points along the line
                b = 0
                f = player.rect.x + (player.rect.width / 2)
                g = player.rect.y + (player.rect.height / 2)
                while b < 10:
                    b += 2
                    f = f + (math.cos(angle) * 2);
                    g = g + (math.sin(angle) * 2);
                    pygame.draw.line(draw_screen, (255,0,0), [f, g], [f, g] )
#======== End of section ===========


        # UI elements
        # Score
        text = str(score)
        game_text(text, 160, 10, True)


            # Scale the draw screen to display screen
        screen.blit(pygame.transform.scale(draw_screen, screen.get_rect().size), (0, 0) ) 
            # place the screen on the display via pygame
        pygame.display.flip()

            # Limit to 60 fps
        clock.tick(60)

    # Out of the Game Loop
    pygame.mixer.music.stop() # Stop the music playlist


''' Call the main function
    This section is important because it tells Python what to call when it is run
'''
if __name__ == '__main__':
    main()
 
# Gracefully shutdown PyGame
pygame.quit()