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
from inc_PlayerHitbox import PlayerHitbox
from inc_Enemy import Enemy
from inc_Lasers import Lasers
from inc_Level import Level
from inc_Shrapnel import Shrapnel
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
background_image = ''

#darkness_image = pygame.image.load("assets/Images/darkness.png").convert_alpha()
darkness_image = pygame.image.load("assets/Images/subtle_darkness.png").convert_alpha() # Not as dark

# Load the font and set the font size
gametext = GameText(configure.canvas, "assets/Fonts/upheavtt.ttf", 14)

# Initialize Controls
controls = Controls(configure)

# Setup "floating" sub windows; used for subscreens
modal = Modal(configure)

# Setup the sprites
player = Player() # player (from the inc_Player.py class)
player_hitbox = PlayerHitbox() # initialize the player's hitbox, a 4x4px square in the middle of player's sprite

    # Sprite Groups are used for multiples of the same thing
enemy_list = pygame.sprite.Group() # Group of all enemy sprites
laser_list = pygame.sprite.Group() # Group of all laser sprites
shrapnel_list = pygame.sprite.Group() # Group of all shrapnel sprites

    # -- Screen Setups
title_screen = Title(configure, gametext)


''' ----- Main Game Loop -----
    Everything happens here!
'''
def game():
    # startup variables
    player_fire_button = 'UP' # Polling Key State

    # Setup the level; this should also nuke any previous level data
    level_data = Level()

    # Prepare the sprite groups, make sure they are empty (good to do for new levels)
    enemy_list.empty()
    laser_list.empty()
    shrapnel_list.empty()

    game_loop = True # Flag used to keep the game loop going
    score = 0 # Player's score!
    graze = 0 # Player's score for "close calls"

    # Start the music loop
        # Enable music Loop by passing -1 to "repeat"
    pygame.mixer.music.play( -1 ) # Starts the music

    # Actual game loop
    while game_loop:
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

        # Key Polling, handles "key up" and "key down" actions
        key = pygame.key.get_pressed()
        # Player "Fire" button
        if player.alive == True:
            if key[pygame.K_SPACE] == True: # pressing button
                if player_fire_button == 'UP':
                    player_fire_button = 'PRESSED'

                if player.gun_loaded == 1:
                    if player.ammo_type == 0:
                        player.fire_delay = 200
                    if player.ammo_type == 1:
                        laser = Lasers(player.rect.x + 16, player.rect.y + 4, enemy_list, player.ammo_type, True)
                        laser.y_force = 1
                        laser_list.add(laser)
                        laser = Lasers(player.rect.x + 16, player.rect.y + 4, enemy_list, player.ammo_type, True)
                        laser.y_force = -1
                        laser_list.add(laser)
                        player.fire_delay = 500
                    if player.ammo_type == 2:
                        player.fire_delay = 300
                    if player.ammo_type == 3:
                        player.fire_delay = 400
                    if player.ammo_type == 4:
                        player.laser_part -= 1
                        if player.laser_part < 1:
                            player.laser_part = 5
                            player.fire_delay = 1000
                        else:
                            player.fire_delay = 50

                    player.gun_loaded = 0 # disable flag
                    configure.play(0); # Play the SFX

                    # Initialize a new laser, and add it to the group
                    laser = Lasers(player.rect.x + 16, player.rect.y + 4, enemy_list, player.ammo_type, True)
                    laser_list.add(laser)

            elif key[pygame.K_SPACE] == False: # released button
                if player_fire_button == 'DOWN':
                    player_fire_button = 'RELEASE'

        player.animation_status = 'MIDDLE'
        if key[pygame.K_LEFT]:
            player.move_left()
        if key[pygame.K_RIGHT]:
            player.move_right()
        if key[pygame.K_UP]:
            player.move_up()
        if key[pygame.K_DOWN]:
            player.move_down()

        # -- Game Logic --
        level_data.increment()

        # Add stars to the screen (background effect using "shrapnel")
        if level_data.starfield_active:
            for shrap in shrapnel_list:
                if shrap.type == 4: # adjust speed of stars if the scene changes
                    if level_data.starfield_speed == 'slow':
                        if shrap.x_force < -10:
                            shrap.x_force += 0.1
                    if level_data.starfield_speed == 'medium':
                        if shrap.x_force < -25:
                            shrap.x_force += 0.1
                        if shrap.x_force > -10:
                            shrap.x_force -= 0.1
                    if level_data.starfield_speed == 'fast':
                        if shrap.x_force > -25:
                            shrap.x_force -= 0.1
                        
            if level_data.starfield_flag:
                level_data.starfield_flag = False
                rect = pygame.Rect( (320, random.randrange(0,240)), (1, 1))
                shrap = Shrapnel(4, rect ) # "laser" shrapnel
                shrap.x_force = level_data.starfield_velocity
                shrap.frame = random.randrange(0, 5)
                shrap.rotation_speed = 0
                shrap.angle = 0
                shrapnel_list.add(shrap)


            # Enemies
        if level_data.enemy_flag != False: # spawn an enemy
            enemy = Enemy(level_data.enemy_flag['type'], level_data.enemy_flag['x'], level_data.enemy_flag['y']);
            enemy_list.add(enemy)
            level_data.enemy_flag = False


        # Enemy fire laser - bullet patterns go here
        for enemy_ship in enemy_list:
            if enemy_ship.gun_loaded == 1:
                enemy_ship.gun_loaded = 0
                if enemy_ship.gun_type == 'straight':
                    # Initialize a new laser, and add it to the group
                    laser = Lasers(enemy_ship.rect.x, enemy_ship.rect.y, False, 5, False)
                    laser.x_force = -2
                    laser_list.add(laser)
                if enemy_ship.gun_type == 'spiral':
                    laser = Lasers(enemy_ship.rect.x, enemy_ship.rect.y, False, 5, False)
                    laser.angle = enemy_ship.gun_angle
                    enemy_ship.gun_angle += 10
                    laser.speed = 1
                    laser.x_force = float(laser.speed * math.cos(math.radians(laser.angle)))
                    laser.y_force = float(laser.speed * math.sin(math.radians(laser.angle)))
                    laser_list.add(laser)
                if enemy_ship.gun_type == 'random':
                    laser = Lasers(enemy_ship.rect.x, enemy_ship.rect.y, False, 5, False)
                    laser.angle = random.randrange(0, 360)
                    laser.speed = 1
                    laser.x_force = float(laser.speed * math.cos(math.radians(laser.angle)))
                    laser.y_force = float(laser.speed * math.sin(math.radians(laser.angle)))
                    laser_list.add(laser)
                if enemy_ship.gun_type == 'circle':
                    for x in range(0, 360, 10): # start, stop, step; change "step" for circle tightness
                        laser = Lasers(enemy_ship.rect.x, enemy_ship.rect.y, False, 5, False)
                        laser.angle = x
                        laser.speed = 1
                        laser.x_force = float(laser.speed * math.cos(math.radians(laser.angle)))
                        laser.y_force = float(laser.speed * math.sin(math.radians(laser.angle)))
                        laser_list.add(laser)
                if enemy_ship.gun_type == 'golden_rule': # lol don't use this
                    for x in range(0, 360, 5): # start, stop, step; change "step" for circle tightness
                        laser = Lasers(enemy_ship.rect.x, enemy_ship.rect.y, False, 5, False)
                        laser.angle = x
                        laser.speed = (math.pi * math.radians(x))
                        laser.x_force = float(laser.speed * math.cos(math.radians(laser.angle)))
                        laser.y_force = float(laser.speed * math.sin(math.radians(laser.angle)))
                        laser_list.add(laser)




            # Player touch powerup (full sprite)
        enemy_hit_list = pygame.sprite.spritecollide(player, enemy_list, False, pygame.sprite.collide_mask)
        for enemy in enemy_hit_list: 
            if enemy.type > 0 and enemy.type < 5:
                configure.play(1); # sfx
                controls.rumble(configure.controller_rumble_id, 100);
                for x in range(5): # pick up powerup
                    shrap = Shrapnel(2, enemy.rect ) # "laser" shrapnel
                    shrap.x_force = random.randrange(-10, 10) / 10
                    shrap.y_force = random.randrange(-10, 10) / 10
                    shrapnel_list.add(shrap)
                player.ammo_type = enemy.type
                enemy.kill()

                # Handle "graze"; it's a sprite overlap but doesn't kill the player
            if enemy.type > 9 and player.alive:
                graze += 1

            # Player touch enemy (hitbox only)
        enemy_hit_list = pygame.sprite.spritecollide(player_hitbox, enemy_list, False, pygame.sprite.collide_mask)
        for enemy in enemy_hit_list: 
            if enemy.type > 9 and player.alive:
                configure.play(1); # sfx
                controls.rumble(configure.controller_rumble_id, 100);
                for x in range(72): # player explode
                    shrap = Shrapnel(1, player.rect ) # "ship" shrapnel
                    shrap.x_force = random.randrange(-40, 40) / 10
                    shrap.y_force = random.randrange(-40, 40) / 10
                    shrapnel_list.add(shrap)
                for x in range(17): # enemy explode
                    shrap = Shrapnel(3, enemy.rect ) # "enemy" shrapnel
                    shrap.x_force = random.randrange(-20, 20) / 10
                    shrap.y_force = random.randrange(-20, 20) / 10
                    shrapnel_list.add(shrap)
                player.death()
                enemy.die()

        # Hit detection
        # Player crash into terrain (no graze bonus here lol)
        player_crash = pygame.sprite.spritecollide(player_hitbox, level_data.objects, False, pygame.sprite.collide_mask)
        for crash in player_crash:
            if crash.collide == True and player.alive and player.invincible_timer == 0:
                controls.rumble(configure.controller_rumble_id, 1000);
                player.death()
                for x in range(72):
                    shrap = Shrapnel(1, player.rect ) # "ship" shrapnel
                    shrap.x_force = random.randrange(-40, 40) / 10
                    shrap.y_force = random.randrange(-40, 40) / 10
                    shrapnel_list.add(shrap)

        # Lasers
        for laser in laser_list:
            if laser.player_laser == True: # Player laser hit enemy
                enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_list, False, pygame.sprite.collide_mask)
                for enemy in enemy_hit_list: 
                    if enemy.type > 9:
                        shrap = Shrapnel(2, laser.rect ) # "laser" shrapnel
                        shrapnel_list.add(shrap)
                        if player.ammo_type != 4:
                            laser.kill()
                        enemy.life -= 1
                        if enemy.life < 1:
                            enemy.die()
                            score += 100
                            configure.play(1); # sfx
                            controls.rumble(configure.controller_rumble_id, 100);
                            shrap = Shrapnel(2, enemy.rect ) # "laser" shrapnel
                            shrapnel_list.add(shrap)
                            for x in range(17):
                                shrap = Shrapnel(3, enemy.rect ) # "enemy" shrapnel
                                shrap.x_force = random.randrange(-20, 20) / 10
                                shrap.y_force = random.randrange(-20, 20) / 10
                                shrapnel_list.add(shrap)


            if laser.player_laser == False: # Enemy Laser hits Player
                if pygame.sprite.collide_mask(laser, player_hitbox):
                    if player.alive and player.invincible_timer == 0:
                        player.death()
                        for x in range(72):
                            shrap = Shrapnel(1, player.rect ) # "ship" shrapnel
                            shrap.x_force = random.randrange(-40, 40) / 10
                            shrap.y_force = random.randrange(-40, 40) / 10
                            shrapnel_list.add(shrap)
                if pygame.sprite.collide_mask(laser, player): # graze
                    if player.alive:
                        graze += 1
                        
            # Laser hits terrain                        
            laser_crash = pygame.sprite.spritecollide(laser, level_data.objects, False, pygame.sprite.collide_mask)
            for crash in laser_crash:
                if crash.collide == True:
                    shrap = Shrapnel(2, laser.rect ) # "laser" shrapnel
                    shrapnel_list.add(shrap)
                    if player.ammo_type != 4:
                        laser.kill()

        # Handle Player-specific timers here
        if player.alive == False:
            if pygame.time.get_ticks() > player.alive_timer:
                if player.lives > 0:
                    player.respawn()
                else: # Game Over
                    game_loop = False 
        else:
            if pygame.time.get_ticks() > player.invincible_timer:
                player.invincible_timer = 0

        # -- Sprite and Screen --
            # Call "update" for sprites
        player.update()
        player_hitbox.update(player.rect)
        level_data.update()
            # "update" the sprite groups
        enemy_list.update()
        laser_list.update()
        shrapnel_list.update()


        # Screen Update
            # Draw the background
        if level_data.background_active:
            if level_data.background_loaded == False:
                background_image = pygame.image.load(level_data.background_file).convert()
            configure.canvas.blit(background_image, [0, 0])
        else:
            configure.canvas.fill((0,0,0))

            # Fading effect
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(level_data.fade_level)
        fade_surface.fill(level_data.fade_color)
        configure.canvas.blit(fade_surface, (0,0))

        # Draw the sprites
            # Note that these are drawn in the order they are called (overlap!)

        # The reason why we do this is so that we can call the modified draw() in Enemy class                
        for enemy in enemy_list:
            enemy.draw(configure.canvas)
        for shrapnel in shrapnel_list:
            # The reason why we do this is so that we can call the modified draw() in Enemy class
            shrapnel.draw(configure.canvas)
        # Normal sprite group draw() with no modification
        player.draw(configure.canvas)
        player_hitbox.draw(configure.canvas, player.invincible_timer)
        level_data.draw(configure.canvas)

#======== This section completely optional ========== Trigonometry is fun!
        if player.ammo_type == 3: # Targeting laser
            # Check to make sure there is, ya know, actually an enemy out there (not a powerup!)
            target_enemy = False
            for enemy in enemy_list:
                if enemy.type > 9:
                    target_enemy = True
                    break

            if target_enemy == True:
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
                    #mpygame.draw.line(configure.canvas, (55, 55, 55), (start_x, start_y), (end_x, end_y) )

                    '''
                    # Draw Green "points" along the line (calculated way to do it!)
                    b = 0
                    speed = distance / 10
                    f = start_x
                    g = start_y
                    while b < distance:
                        b += speed
                        f = f + (math.cos(angle) * speed);
                        g = g + (math.sin(angle) * speed);
                        pygame.draw.line(configure.canvas, (0, 255, 0), [f, g], [f, g] )
                    '''

                    # Check if this is the closest distance (used for 'red line' below, outside of loop)
                    if distance < closest and enemy.type > 9:
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
                    pygame.draw.line(configure.canvas, (255,0,0), [f, g], [f, g] )
#======== End of section ===========

        #===== Darkness Effect ===== probably need to move this to inc_Level.py
            # Draw the "darkness"
        if level_data.darkness_scale != 0:
            rect = darkness_image.get_rect()
            if pygame.time.get_ticks() > level_data.darkness_timer + 10:
                level_data.darkness_timer = pygame.time.get_ticks()
                if level_data.darkness_flag == True and level_data.darkness_scale > 100:
                    level_data.darkness_scale -= 1
                elif level_data.darkness_flag == False and level_data.darkness_scale < 300:
                    level_data.darkness_scale += 1

            # Apply scaling
            width = rect.width * (level_data.darkness_scale / 100)
            height = rect.height * (level_data.darkness_scale / 100)

            scaled_darkness_image = pygame.transform.scale(darkness_image, (width, height) )

            # Center to the player's position
            rect = scaled_darkness_image.get_rect(center = player.rect.center)            
            configure.canvas.blit(scaled_darkness_image, rect)

            if level_data.darkness_scale == 301:
                level_data.darkness_scale = 0

        #===== End Darkness Effect =====

            # Draw lasers outside of the "darkness" since they are their own light source and shouldn't fade
        laser_list.draw(configure.canvas)

        # UI elements
        # Score
        text = "Score: " + str(score)
        gametext.text(text, 160, 10, True, False)
        text = "Graze: " + str(graze)
        gametext.text(text, 160, 0, True, False)

        text = str(level_data.distance)
        gametext.text(text, 300, 220, True, False)

        # Player Lives
        for x in range(player.lives):
            configure.canvas.blit(player.animation_frames[0], [x * 17, 220])

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