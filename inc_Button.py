import pygame

# ----- Import from other files ----
from inc_GameText import GameText

# ----- Classes -----
''' Button
    Manages all Button behavior and drawing

'''
class Button(object):

    def __init__(self, configure, name, x, y, font_size, centered = False):

        self.configure = configure

        self.name = name
            # rect
        self.x = x
        self.y = y
        self.width = len(name) * font_size
        self.height = font_size
        self.centered = 0
        if centered:
            self.centered = self.width / 2

        # Font, hard coded size 
        self.gametext = GameText(self.configure.canvas, "assets/Fonts/upheavtt.ttf", 14 )

        self.is_visible = True
        self.is_active = False
        self.is_hover = False

    def click(self, mouse_x, mouse_y):
        self.is_active = False

        if self.centered != False:
            if mouse_x > self.x - (self.centered) and mouse_x < self.x + self.width - (self.centered) and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_active = True
        else:
            if mouse_x > self.x - 2 and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_active = True


    def hover(self, mouse_x, mouse_y):
        self.is_hover = False

        if self.centered != False:
            if mouse_x > self.x - (self.centered) and mouse_x < self.x + self.width - (self.centered) and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_hover = True
        else:
            if mouse_x > self.x - 2 and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_hover = True

    def draw(self):

        # Button background, changes on status
        if self.is_hover or self.is_active:
            pygame.draw.rect(self.configure.canvas, (200, 200, 200), (self.x - (self.centered ), self.y, self.width, self.height) )
        else:
            pygame.draw.rect(self.configure.canvas, (175, 175, 175), (self.x - (self.centered ), self.y, self.width, self.height) )

        # Button border
        pygame.draw.rect(self.configure.canvas, (130, 120, 130), (self.x - (self.centered ), self.y, self.width, self.height), 1 )

        self.gametext.text( self.name, self.x - (self.centered / 2), self.y, False, False)
