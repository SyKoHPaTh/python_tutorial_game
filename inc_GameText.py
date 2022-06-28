import pygame
import random

# ----- Classes -----
''' GameText
    Class used to load and position text on a screen

    text
        Objective
            Handles the fancy stuff for placing pretty text on the screen
        Parameter
            text    the text we want to display
            x       x location of the text
            y       y location of the text
            centered    do fancy math to place the text centered at x

    Note use of FONT:
        .size(text)     (width, height), using [0] for teh width / 2 = centered text
        .get_linesize() for multiline text, use this

'''
class GameText(object):

    def __init__(self, screen, file_name, font_size):
        self.font = pygame.font.Font(file_name, font_size)
        self.screen = screen

    def text(self, text, x, y, centered, flashing):

        if isinstance(text, list):
            for line in text:
                if centered == True:
                    pos_x = x - (self.font.size(text)[0]) / 2

                text_render_bg = self.font.render(line, True, (50, 50, 50)) 

                if flashing == True:
                    flash = random.randrange(1, 3)
                    if flash == 1: text_render = self.font.render(line, True, (85, 255, 255)) 
                    if flash == 2: text_render = self.font.render(line, True, (255, 255, 85)) 
                    if flash == 3: text_render = self.font.render(line, True, (255, 255, 255)) 
                else:
                    text_render = self.font.render(line, True, (200, 200, 200)) 



                self.screen.blit(text_render_bg, [ (pos_x + 1), (y + 1)])
                self.screen.blit(text_render, [pos_x, y])
                    # adjust next line
                y += self.font.get_linesize()

        else:
            if centered == True:
                x -= (self.font.size(text)[0]) / 2

            text_render_bg = self.font.render(text, True, (50, 50, 50)) 

            if flashing == True:
                flash = random.randrange(1, 3)
                if flash == 1: text_render = self.font.render(text, True, (85, 255, 255)) 
                if flash == 2: text_render = self.font.render(text, True, (255, 255, 85)) 
                if flash == 3: text_render = self.font.render(text, True, (255, 255, 255)) 
            else:
                text_render = self.font.render(text, True, (200, 200, 200)) 

            self.screen.blit(text_render_bg, [ (x + 1), (y + 1)])
            self.screen.blit(text_render, [x, y])

