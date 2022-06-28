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
from inc_Modal import Modal
from inc_Configure import Configure
from inc_GameText import GameText
from inc_Controls import Controls

from screen_Title import Title
# ----- Initialization -----
# set Environment variables; default initial Window Position
x = 0
y = 30
#calculate the "middle"
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) # absolute window positioning
os.environ['SDL_VIDEO_CENTERED'] = '1' # Use this option to center the window when it is created

# Call this function so the Pygame library can initialize itself
pygame.init()

# Canvas size, we draw to this "screen" and then it scales and displays on the screen
    # This is "classic arcade" size screen; big pixels, old school
WIDTH = 320
HEIGHT = 240

# Initialize configuration
configure = Configure(WIDTH, HEIGHT)

    # Window icon
icon = pygame.image.load("assets/Images/icon.png")
pygame.display.set_icon(icon)

# Hide the mouse
pygame.mouse.set_visible(False)
 
# This sets the name of the window
pygame.display.set_caption('Tutorial Spaceship Shooter')
  
# Clock is used to cap framerate
clock = pygame.time.Clock()

# Load static images
background_image = pygame.image.load("assets/Images/background.png").convert()

# Load the font and set the font size
gametext = GameText(configure.canvas, "assets/Fonts/upheavtt.ttf", 14)

# Initialize Controls
controls = Controls(configure)

# Setup "floating" sub windows; used for subscreens
modal = Modal(configure)

# Setup the sprites
player = Player() # player (from the inc_Player.py class)
terrain_ceiling = Terrain(0) # the terrain ceiling
terrain_ground = Terrain(1) # the terrain ground

    # Sprite Groups are used for multiples of the same thing
enemy_list = pygame.sprite.Group() # Group of all enemy sprites
laser_list = pygame.sprite.Group() # Group of all laser sprites

    # -- Screen Setups
title_screen = Title(configure, gametext)


''' ----- Main Game Loop -----
    Everything happens here!
'''
def game():
    # startup variables
        # how often enemies appear
    enemy_spawn_timer = pygame.time.get_ticks() + 9000 # extra delay (9seconds)
    player_fire_button = 'UP' # Polling Key State

    # Prepare the sprite groups, make sure they are empty (good to do for new levels)
    enemy_list.empty()
    laser_list.empty()

    player_alive = True # Flag used to keep the game loop going
    score = 0 # Player's score!

    # Start the music loop
        # Enable music Loop by passing -1 to "repeat"
    pygame.mixer.music.play( -1 ) # Starts the music

    # Actual game loop
    while player_alive:
        # -- Event handler --
        key_list = controls.get_key()
        # loop through key dist
        for key in key_list:
            if key['label'] == 'QUIT':
                return "quit"
            if key['label'] == 'Menu':
                status = modal.pause()
                if status == 'quit':
                    return 'quit'

        # Polling = keys being held down
        polling_list = controls.get_key_pressed()
        for key_pressed in polling_list:
            # Player "Fire" button
            if key_pressed['label'] == 'Fire': # pressing button
                if key_pressed['value'] == True:
                    if player_fire_button == 'UP':
                        player_fire_button = 'PRESSED'

                    if player.gun_loaded == 1:
                        player.gun_loaded = 0 # disable flag
                        configure.play(0); # Play the SFX stored in index 0

                        # Initialize a new laser, and add it to the group
                        laser = Lasers()
                        laser.rect.x = player.rect.x
                        laser.rect.y = player.rect.y
                        laser.type = 0 # flag saying it is a player's laser
                        laser_list.add(laser)

                        controls.rumble(configure.controller_rumble_id, 10);


                else: # released button
                    if player_fire_button == 'DOWN':
                        player_fire_button = 'RELEASE'

            # Movement
            if key_pressed['value'] == True:
                if key_pressed['label'] == 'Up':
                    player.move_up()
                if key_pressed['label'] == 'Down':
                    player.move_down()
                if key_pressed['label'] == 'Left':
                    player.move_left()
                if key_pressed['label'] == 'Right':
                    player.move_right()


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
            player_alive = False # Break the game loop flag = game over
            controls.rumble(configure.controller_rumble_id, 1000);

            # Lasers
        for laser in laser_list:
            if laser.type == 0: # Player laser hit enemy
                enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_list, False, pygame.sprite.collide_mask)
                for enemy in enemy_hit_list:
                    if enemy.alive:
                        enemy.alive = False
                        score += 100
                        configure.play(1); # sfx
                        laser.kill()
                        controls.rumble(configure.controller_rumble_id, 100);

            if laser.type == 1: # Enemy Laser hits Player
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
        configure.canvas.blit(background_image, [0, 0])
            # Draw the sprites
                # Note that these are drawn in the order they are called (overlap!)
        enemy_list.draw(configure.canvas)
        laser_list.draw(configure.canvas)
        player.draw(configure.canvas)
        terrain_ceiling.draw(configure.canvas)
        terrain_ground.draw(configure.canvas)

        # UI elements
        # Score
        text = str(score)
        gametext.text(text, 160, 10, True, False)

        configure.display()

            # Limit to 60 fps
        clock.tick(60)

    # Out of the Game Loop
    pygame.mixer.music.stop() # Stop the music playlist

    return 'title'


# ----- Main Loop
def main():
    done = False

    action = "title"

    # Screen looping: Title -> Demo -> HighScores ...
    while not done:
        if action == 'quit':
            done = True
        elif action == "title":
            action = title_screen.display()
        elif action == "gameplay":
            action = game()
        #elif action == "demo":
        #    action = demo() # This could be a function that shows demo gameplay
        #elif action == "highscores":
        #    action = high_scores() # This could show a high scores screen


''' Call the main function
    This section is important because it tells Python what to call when it is run
'''
if __name__ == '__main__':
    main()
 

# Gracefully shutdown PyGame
pygame.quit()