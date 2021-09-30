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

# ---- File Includes ----
from inc_Player import Player
from inc_Enemy import Enemy
from inc_Lasers import Lasers
from inc_Terrain import Terrain
from inc_Shrapnel import Shrapnel

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
shrapnel_list = pygame.sprite.Group() # Group of all shrapnel sprites

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
    shrapnel_list.empty()

    game_loop = True # Flag used to keep the game loop going
    score = 0 # Player's score!

    # Start the music loop
        # Enable music Loop by passing -1 to "repeat"
    pygame.mixer.music.play( -1 ) # Starts the music

    # Actual game loop
    while game_loop:
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
                laser = Lasers()
                laser.rect.x = player.rect.x
                laser.rect.y = player.rect.y
                laser.type = 0 # flag saying it is a player's laser
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
                laser = Lasers() 
                laser.rect.x = enemy_ship.rect.x
                laser.rect.y = enemy_ship.rect.y
                laser.type = 1 # flag saying it is a enemy's laser
                laser_list.add(laser)

        # Hit detection
            # Player crash into terrain
            if pygame.sprite.collide_mask(player, terrain_ceiling) or pygame.sprite.collide_mask(player, terrain_ground):
                if player.alive:
                    for x in range(72):
                        shrap = Shrapnel(1, player.rect.x, player.rect.y ) # "ship" shrapnel
                        shrap.x_force = random.randrange(-40, 40) / 10
                        shrap.y_force = random.randrange(-40, 40) / 10
                        shrapnel_list.add(shrap)
                player.death()

            # Lasers
            for laser in laser_list:
                if laser.type == 0: # Player laser hit enemy
                    enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_list, False, pygame.sprite.collide_mask)
                    for enemy in enemy_hit_list: 
                        if enemy.alive:
                            enemy.alive = False
                            score += 100
                            sfx_enemy_die.play(); # sfx
                            shrap = Shrapnel(2, enemy.rect.x, enemy.rect.y ) # "laser" shrapnel
                            shrapnel_list.add(shrap)
                            for x in range(17):
                                shrap = Shrapnel(3, enemy.rect.x, enemy.rect.y ) # "laser" shrapnel
                                shrap.x_force = random.randrange(-20, 20) / 10
                                shrap.y_force = random.randrange(-20, 20) / 10
                                shrapnel_list.add(shrap)

                            laser.kill()
                if laser.type == 1: # Enemy Laser hits Player
                    if pygame.sprite.collide_mask(laser, player):
                        if player.alive:
                            for x in range(72):
                                shrap = Shrapnel(1, player.rect.x, player.rect.y ) # "ship" shrapnel
                                shrap.x_force = random.randrange(-40, 40) / 10
                                shrap.y_force = random.randrange(-40, 40) / 10
                                shrapnel_list.add(shrap)
                        player.death()
                # Laser hits terrain                        
                if pygame.sprite.collide_mask(laser, terrain_ceiling) or pygame.sprite.collide_mask(laser, terrain_ground):
                    shrap = Shrapnel(2, laser.rect.x, laser.rect.y ) # "laser" shrapnel
                    shrapnel_list.add(shrap)
                    laser.kill()

        if player.alive == False:
            if pygame.time.get_ticks() > player.alive_timer + 5000:
                game_loop = False

        # -- Sprite and Screen --
            # Call "update" for sprites
        player.update()
        terrain_ceiling.update()
        terrain_ground.update()
            # "update" the sprite groups
        enemy_list.update()
        laser_list.update()
        shrapnel_list.update()


        # Screen Update
            # Draw the background
        draw_screen.blit(background_image, [0, 0])
            # Draw the sprites
                # Note that these are drawn in the order they are called (overlap!)
        enemy_list.draw(draw_screen)
        laser_list.draw(draw_screen)
        player.draw(draw_screen)
        terrain_ceiling.draw(draw_screen)
        terrain_ground.draw(draw_screen)
        shrapnel_list.draw(draw_screen)

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