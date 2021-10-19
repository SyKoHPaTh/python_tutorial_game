import pygame

# ----- Import from other files ----
from inc_GameText import GameText
from inc_Menu import Menu

# ----- Classes -----
''' Alert Box
    Handles all Pop up / Confirm boxes

'''

class Alertbox():

    def __init__(self, configure):
        super().__init__()

        # Font, hard coded size 
        self.gametext = GameText(configure.canvas, "assets/Fonts/upheavtt.ttf", 14 )

        self.configure = configure # holds configuration settings

        # Initialize buttons (these are used for all modals)
        self.button_group = []
        self.button_group.append( Menu('Ok', 225, 275, 12) )
        self.button_group.append( Menu('Cancel', 300, 275, 12) )



    def alert(self, message, ok_button, cancel_button):

        buttons = 0
        if ok_button or cancel_button:
            buttons = 1
        if ok_button and cancel_button:
            buttons = 2

        # adjust buttons
        for item in self.button_group:
            if item.name == 'Ok':
                if buttons == 1:
                    item.x = 300
                if buttons == 2:
                    item.x = 225
                item.y = 275
                item.is_visible = ok_button
                item.is_active = False
            if item.name == 'Cancel':
                if buttons == 1:
                    item.x = 275
                if buttons == 2:
                    item.x = 300
                item.y = 275
                item.is_visible = cancel_button
                item.is_active = False


        wait_for_response = True
        while wait_for_response:
            mpos_x, mpos_y = pygame.mouse.get_pos() # current mouse position


            # ----- Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # did the user click the 'x' to close the window
                    return False
                if event.type == pygame.KEYDOWN:

                    if ok_button:
                        if event.key == pygame.K_RETURN:
                            return True

                    if cancel_button:
                        if event.key == pygame.K_ESCAPE:
                            return False

                    # events for just clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB
                        for item in self.button_group:
                            item.click(mpos_x, mpos_y)
                            if item.name == 'Ok' and item.is_active:
                                return True
                            if item.name == 'Cancel' and item.is_active:
                                return False


            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (150, 200, 300, 100 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (150, 200, 300, 100 ), 5)

            # Text
            self.gametext.text( message , 300, 210, True, False, False)

            for item in self.button_group:
                if item.is_visible:
                    item.hover(mpos_x, mpos_y)
                    if item.is_hover or item.is_active:
                        self.gametext.text( item.name, item.x, item.y, False, False, (230, 220, 230))
                    else:
                        self.gametext.text( item.name, item.x, item.y, False, False, (130, 120, 130))

            self.configure.display()

    def input(self, message, ok_button, cancel_button, pre_text):

        buttons = 0
        if ok_button or cancel_button:
            buttons = 1
        if ok_button and cancel_button:
            buttons = 2

        # adjust buttons
        for item in self.button_group:
            if item.name == 'Ok':
                if buttons == 1:
                    item.x = 300
                if buttons == 2:
                    item.x = 225
                item.y = 275
                item.is_visible = ok_button
                item.is_active = False
            if item.name == 'Cancel':
                if buttons == 1:
                    item.x = 275
                if buttons == 2:
                    item.x = 300
                item.y = 275
                item.is_visible = cancel_button
                item.is_active = False


        wait_for_response = True
        while wait_for_response:
            mpos_x, mpos_y = pygame.mouse.get_pos() # current mouse position


            # ----- Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # did the user click the 'x' to close the window
                    return False
                if event.type == pygame.KEYDOWN:

                    if ok_button:
                        if event.key == pygame.K_RETURN:
                            return pre_text

                    if cancel_button:
                        if event.key == pygame.K_ESCAPE:
                            return False

                    if event.key == pygame.K_BACKSPACE:
                        pre_text = pre_text[:-1]
                    else:
                        pre_text += event.unicode                            

                    # events for just clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB
                        for item in self.button_group:
                            item.click(mpos_x, mpos_y)
                            if item.name == 'Ok' and item.is_active:
                                return pre_text
                            if item.name == 'Cancel' and item.is_active:
                                return False



            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (150, 200, 300, 100 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (150, 200, 300, 100 ), 5)

                # input background
            pygame.draw.rect(self.configure.canvas, (0, 0, 0), (160, 226, 280, 28 ))
                # input border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (160, 226, 280, 28 ), 2)


           # Text
            self.gametext.text( message, 300, 210, True, False, False)
            self.gametext.text( pre_text, 300, 232, True, False, False)

            for item in self.button_group:
                if item.is_visible:
                    item.hover(mpos_x, mpos_y)
                    if item.is_hover or item.is_active:
                        self.gametext.text( item.name, item.x, item.y, False, False, (230, 220, 230))
                    else:
                        self.gametext.text( item.name, item.x, item.y, False, False, (130, 120, 130))

            self.configure.display()


    def progress_bar(self, message, progress):

        # Draw stuff
            # modal background
        pygame.draw.rect(self.configure.canvas, (155, 155, 155), (150, 200, 300, 100 ))
            # modal border
        pygame.draw.rect(self.configure.canvas, (130, 120, 130), (150, 200, 300, 100 ), 5)

        # Text
        self.gametext.text( message , 300, 210, True, False, False)

        # progress bar
        self.gametext.text( str(progress) , 300, 230, True, False, False)

        self.configure.display()

    ''' Pause Screen
        Resume
        Configure
            -> Display, Audio, Controls (->key remap)
        Exit Game
    '''
    def pause(self):
        print("generic pause screen")

        # Show the mouse (we need to click the buttons!)
        pygame.mouse.set_visible(True)

        # Initialize buttons
        menu_buttons = []
        menu_buttons.append( Menu('Resume', 170, 50, 14, True) )
        menu_buttons.append( Menu('Configure', 170, 100, 14, True) )
        menu_buttons.append( Menu('Exit', 170, 150, 14, True) )

        for item in menu_buttons:
            item.is_visible = True


        status = 'quit'


        wait_for_response = True
        while wait_for_response:
            mpos_x, mpos_y = pygame.mouse.get_pos() # current mouse position
            # adjust for screen size scaling
            mpos_x = mpos_x / (self.configure.screen_width / self.configure.canvas.get_width())
            mpos_y = mpos_y / (self.configure.screen_height / self.configure.canvas.get_height())


            # ----- Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # did the user click the 'x' to close the window
                    wait_for_response = False
                    status = 'quit'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        wait_for_response = False
                        status = 'resume'

                    # events for just clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB
                        for item in menu_buttons:
                            item.click(mpos_x, mpos_y)
                            if item.name == 'Resume' and item.is_active:
                                wait_for_response = False
                                status = 'resume'
                            if item.name == 'Configure' and item.is_active:
                                wait_for_response = False
                                status = 'configure'
                            if item.name == 'Exit' and item.is_active:
                                wait_for_response = False
                                status = 'quit'



            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (110, 25, 200, 175 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (110, 25, 200, 175 ), 5)


           # Draw the menu buttons
            for item in menu_buttons:
                if item.is_visible:
                    item.hover(mpos_x, mpos_y)
                    if item.is_hover or item.is_active:
                        self.gametext.text( item.name, 170, item.y, True, False, (230, 220, 230))
                    else:
                        self.gametext.text( item.name, 170, item.y, True, False, (130, 120, 130))

            self.configure.display()

        # Hide the mouse
        pygame.mouse.set_visible(False)

        return status

