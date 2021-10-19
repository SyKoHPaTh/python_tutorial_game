
# ----- Classes -----
''' Menu
    Manages all Menu events

'''
class Menu(object):

    def __init__(self, name, x, y, font_size, centered = False):
        self.name = name
            # rect
        self.x = x
        self.y = y
        self.width = len(name) * font_size
        self.height = font_size
        self.centered = centered
        if centered:
            self.centered = x - (self.width / 2)

        self.is_visible = True
        self.is_active = False
        self.is_hover = False

    def click(self, mouse_x, mouse_y):
        self.is_active = False

        if self.centered != False:
            if mouse_x > self.x - (self.centered / 3) and mouse_x < self.x + self.width - (self.centered / 3) and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_active = True
        else:
            if mouse_x > self.x - 2 and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_active = True


    def hover(self, mouse_x, mouse_y):
        self.is_hover = False

        if self.centered != False:
            if mouse_x > self.x - (self.centered / 3) and mouse_x < self.x + self.width - (self.centered / 3) and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_hover = True
        else:
            if mouse_x > self.x - 2 and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height and self.is_visible:
                self.is_hover = True

