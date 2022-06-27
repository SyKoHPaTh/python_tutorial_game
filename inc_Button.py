import pygame

# ----- Import from other files ----
from inc_GameText import GameText

# ----- Classes -----
''' Button
    Manages all Button behavior and drawing

'''
class Button(object):

    def __init__(self, configure, name, x, y, font_size, centered = False):
        self.width = len(name) * font_size
        self.height = font_size

        # Create a Surface that can be interacted with
        self.image = pygame.Surface((self.width, self.height))
        # self.image.fill((0,255,0))

        self.configure = configure

        self.name = name
            # rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.centered = 0
        if centered:
            self.centered = self.width / 2
            self.rect.x = self.rect.x - self.centered

        # Font, hard coded size 
        self.gametext = GameText(self.configure.canvas, "assets/Fonts/upheavtt.ttf", 14 )

        self.is_visible = True
        self.is_active = False
        self.is_hover = False

    def click(self, mouse):
        self.is_active = False

        if self.rect.collidepoint(mouse):
            self.is_active = True
        else:
            self.is_active = False


    def hover(self, mouse):
        self.is_hover = False

        if self.rect.collidepoint(mouse):
            self.is_hover = True
        else:
            self.is_hover = False

    def draw(self):

        # Button background, changes on status
        if self.is_hover or self.is_active:
            pygame.draw.rect(self.configure.canvas, (200, 200, 200), (self.rect.x, self.rect.y, self.width, self.height) )
        else:
            pygame.draw.rect(self.configure.canvas, (175, 175, 175), (self.rect.x, self.rect.y, self.width, self.height) )

        # Button border
        pygame.draw.rect(self.configure.canvas, (130, 120, 130), (self.rect.x, self.rect.y, self.width, self.height), 1 )

        self.gametext.text( self.name, self.rect.x + (self.centered / 2), self.rect.y, False, False)

