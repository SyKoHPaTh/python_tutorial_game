import pygame

# ----- Import from other files ----
from inc_GameText import GameText
from inc_Button import Button
from inc_Controls import Controls

# ----- Classes -----
''' Modal Box
    Handles all Pop up / Confirm boxes

'''

class Modal():

    def __init__(self, configure):
        super().__init__()

        # Font, hard coded size 
        self.gametext = GameText(configure.canvas, "assets/Fonts/upheavtt.ttf", 14 )

        self.configure = configure # holds configuration settings

    ''' Pause Screen
        Resume
        Configure
            -> Display, Audio, Controls (->key remap)
        Exit Game
    '''
    def pause(self):
        # Show the mouse (we need to click the buttons!)
        pygame.mouse.set_visible(True)

        # Initialize buttons
        menu_buttons = []
        menu_buttons.append( Button(self.configure, 'Resume', 160, 50, 14, True) )
        menu_buttons.append( Button(self.configure, 'Configure', 160, 100, 14, True) )
        menu_buttons.append( Button(self.configure, 'Exit', 160, 150, 14, True) )

        status = 'quit' # Status is passed to the calling variable

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
                            item.click( (mpos_x, mpos_y) )
                            if item.name == 'Resume' and item.is_active:
                                wait_for_response = False
                                status = 'resume'
                            if item.name == 'Configure' and item.is_active:
                                status = self.configure_screen()
                                if status == 'quit':
                                    wait_for_response = False
                            if item.name == 'Exit' and item.is_active:
                                wait_for_response = False
                                status = 'quit'

            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (60, 25, 200, 175 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (60, 25, 200, 175 ), 5)


           # Draw the menu buttons
            for item in menu_buttons:
                if item.is_visible:
                    item.hover( (mpos_x, mpos_y) ) # check if the mouse is hovering over the button
                    item.draw() # draw the button

            self.configure.display()

        # Hide the mouse
        pygame.mouse.set_visible(False)

        return status

    ''' Configure Screen
        Sub menu for configuration sub-sub-menus
        also Back just returns to previous screen
    '''
    def configure_screen(self):

        # Initialize buttons
        menu_buttons = []
        menu_buttons.append( Button(self.configure, 'Video', 160, 50, 14, True) )
        menu_buttons.append( Button(self.configure, 'Audio', 160, 70, 14, True) )
        menu_buttons.append( Button(self.configure, 'Controls', 160, 90, 14, True) )
        menu_buttons.append( Button(self.configure, 'Back', 160, 180, 14, True) )

        status = 'resume' # Status is passed to the calling variable

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

                    # events for just clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB
                        for item in menu_buttons:
                            item.click( (mpos_x, mpos_y) )
                            if item.name == 'Video' and item.is_active:
                                status = self.video()
                                if status == 'quit':
                                    wait_for_response = False
                            if item.name == 'Audio' and item.is_active:
                                status = self.audio()
                                if status == 'quit':
                                    wait_for_response = False
                            if item.name == 'Controls' and item.is_active:
                                status = self.controls()
                                if status == 'quit':
                                    wait_for_response = False
                            if item.name == 'Back' and item.is_active:
                                wait_for_response = False

            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (60, 25, 200, 175 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (60, 25, 200, 175 ), 5)


           # Draw the menu buttons
            for item in menu_buttons:
                if item.is_visible:
                    item.hover( (mpos_x, mpos_y) ) # check if the mouse is hovering over the button
                    item.draw() # draw the button

            self.configure.display()

        return status


    ''' Video Configure Screen
        Configuration options for video:
            Fullscreen / Windowed / Borderless Windowed
            Screen size (width and height) = supported display modes only
            Resize fit: stretch, width, height
        Cancel
        Apply -> Applies the configuration options
        Ok -> Apply and go to previous screen
    '''
    def video(self):
        # Video options

        # Determine display options, and figure out which one we're using right now
        display_option = ['Fullscreen', 'Windowed', 'Borderless Window']
        if self.configure.fullscreen == True:
            display_option_select = 0 # Full screen
        elif self.configure.fullscreen == False and self.configure.borderless == False:
            display_option_select = 1 # Windowed
        elif self.configure.fullscreen == False and self.configure.borderless == True:
            display_option_select = 2 # Borderless Window

        # Current display mode: List in format [(height, width)]
        screen_modes = pygame.display.list_modes()

        screen_mode_select = 0 # default to first in list
        counter = 0
        for mode in screen_modes:
            width = mode[0]
            height = mode[1]
            if self.configure.screen_width == width and self.configure.screen_height == height:
                screen_mode_select = counter
            counter += 1

        # List of resize fitments
        resize_fit = ['stretch', 'width', 'height']
        resize_fit_select = resize_fit.index(self.configure.screen_fit)


        # Initialize buttons
        menu_buttons = []
        menu_buttons.append( Button(self.configure, '<', 78, 75, 14, True) )
        menu_buttons.append( Button(self.configure, '>', 242, 75, 14, True) )
        menu_buttons.append( Button(self.configure, 'Cancel', 210, 180, 14, True) )
        menu_buttons.append( Button(self.configure, 'Apply', 160, 130, 14, True) )
        menu_buttons.append( Button(self.configure, 'OK', 110, 180, 14, True) )

        status = 'resume' # Status is passed to the calling variable

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

                    # events for just clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB
                        # Check if an options field was clicked, and actions
                            # Display Option
                        if mpos_x > 70 and mpos_x < 250 and mpos_y > 45 and mpos_y < 59:
                            display_option_select += 1
                            if display_option_select >= len(display_option):
                                display_option_select = 0

                        if mpos_x > 70 and mpos_x < 250 and mpos_y > 105 and mpos_y < 119:
                            resize_fit_select += 1
                            if resize_fit_select >= len(resize_fit):
                                resize_fit_select = 0
                        
                        # Check if button was clicked, and actions
                        for item in menu_buttons:
                            item.click( (mpos_x, mpos_y) )
                            if item.name == '<' and item.is_active:
                                screen_mode_select += 1
                                if screen_mode_select >= len(screen_modes):
                                    screen_mode_select = 0
                            if item.name == '>' and item.is_active:
                                screen_mode_select -= 1
                                if screen_mode_select < 0:
                                    screen_mode_select = len(screen_modes) - 1
                            if item.name == 'Apply' and item.is_active:
                                # Disable button after clicking
                                item.is_active = False
                                item.is_hover = False

                                # Display Window
                                if display_option[display_option_select] == 'Fullscreen':
                                    self.configure.fullscreen = True
                                    self.configure.borderless = False
                                if display_option[display_option_select] == 'Windowed':
                                    self.configure.fullscreen = False
                                    self.configure.borderless = False
                                if display_option[display_option_select] == 'Borderless Window':
                                    self.configure.fullscreen = False
                                    self.configure.borderless = True

                                # Screen fit
                                self.configure.screen_fit = resize_fit[resize_fit_select]

                                # Screen Size
                                self.configure.screen_width = screen_modes[screen_mode_select][0]
                                self.configure.screen_height = screen_modes[screen_mode_select][1]

                                # Re-init the display with current settings
                                self.configure.init_display()
                            if item.name == 'Cancel' and item.is_active:
                                # Load settings from file and re-init display (basically an undo of whatever was changed in this modal)
                                self.configure.load()
                                self.configure.init_display()
                                wait_for_response = False
                            if item.name == 'OK' and item.is_active:
                                # Save applied settings and re-init display (Apply before Ok-ing!)
                                self.configure.save()
                                self.configure.init_display()
                                wait_for_response = False

            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (60, 25, 200, 175 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (60, 25, 200, 175 ), 5)

            # Labels, and selected options text
            self.gametext.text('Display Mode', 80, 30, False, False)
            pygame.draw.rect(self.configure.canvas, (100, 100, 100), (70, 45, 180, 14 ) )
            self.gametext.text( display_option[display_option_select], 80, 45, False, False)

            self.gametext.text('Screen Size', 80, 60, False, False)
            pygame.draw.rect(self.configure.canvas, (100, 100, 100), (80, 75, 160, 14 ) )
            self.gametext.text( str(screen_modes[screen_mode_select][0]) + " x " + str(screen_modes[screen_mode_select][1]), 190, 75, True, False)

            self.gametext.text('Resize Fit to Display', 80, 90, False, False)
            pygame.draw.rect(self.configure.canvas, (100, 100, 100), (70, 105, 180, 14 ) )
            self.gametext.text( resize_fit[resize_fit_select], 80, 105, False, False)

            # Draw the menu buttons
            for item in menu_buttons:
                if item.is_visible:
                    item.hover( (mpos_x, mpos_y) ) # check if the mouse is hovering over the button
                    item.draw() # draw the button

            self.configure.display()

        return status

    ''' Controls Configure Screen
        Configuration options for Controls:
            Key bindings
            [x] Rumble
        Cancel
        Ok -> Save and go to previous screen
    '''
    def controls(self):
        # Controls options
        print("controls")

        controls = Controls(self.configure)

        if self.configure.controller_rumble_id != False:
            rumble_name = controls.get_name(self.configure.controller_rumble_id)
        else:
            rumble_name = 'None'

        #keypress = controls.wait_for_key()
        #print("Pressed: ", keypress['key'])

        #if keypress['id'] != 'keyboard':
        #    name = controls.get_name(keypress['id'])
        #    print("Controller: ", name)
        #    controls.rumble(keypress['id'])


        # Video options

        # Initialize buttons
        menu_buttons = []
        menu_buttons.append( Button(self.configure, 'Cancel', 210, 180, 14, True) )
        menu_buttons.append( Button(self.configure, 'OK', 110, 180, 14, True) )

        status = 'resume' # Status is passed to the calling variable

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

                    # events for just clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB
                        # Check if field was clicked, and reassign button
                        y = 45
                        for row in self.configure.control_map:
                            if mpos_x > 140 and mpos_x < 250 and mpos_y > y and mpos_y < y + 14:
                                pygame.draw.rect(self.configure.canvas, (200, 200, 200), (140, y, 110, 14 ) )
                                pygame.draw.rect(self.configure.canvas, (250, 250, 250), (140, y, 110, 14 ) , 1)
                                self.configure.display()

                                keypress = controls.wait_for_key()
                                label = keypress.pop('label')
                                row.update(keypress)
                            y += 15

                        # Check if Rumble was clicked
                        if mpos_x > 140 and mpos_x < 250 and mpos_y > 150 and mpos_y < 164:
                            pygame.draw.rect(self.configure.canvas, (200, 200, 200), (140, 150, 110, 14 ) )
                            pygame.draw.rect(self.configure.canvas, (250, 250, 250), (140, 150, 110, 14 ) , 1)
                            self.configure.display()

                            keypress = controls.wait_for_key()
                            if keypress['id'] == 'keyboard':
                                keypress['id'] = False
                            self.configure.controller_rumble_id = keypress['id']
                            if self.configure.controller_rumble_id != False:
                                rumble_name = controls.get_name(self.configure.controller_rumble_id)



                        # Check if button was clicked, and actions
                        for item in menu_buttons:
                            item.click( (mpos_x, mpos_y) )
                            if item.name == 'Cancel' and item.is_active:
                                # Load settings from file (don't save control changes)
                                self.configure.load()
                                wait_for_response = False
                            if item.name == 'OK' and item.is_active:
                                # Save settings (save our new control changes)
                                self.configure.save()
                                wait_for_response = False

            # Draw stuff
                # modal background
            pygame.draw.rect(self.configure.canvas, (155, 155, 155), (60, 25, 200, 175 ))
                # modal border
            pygame.draw.rect(self.configure.canvas, (130, 120, 130), (60, 25, 200, 175 ), 5)

            # Labels, and selected options text
            self.gametext.text('Key Remap', 80, 30, False, False)

            # Control Mapping
            y = 45
            for row in self.configure.control_map:
                pygame.draw.rect(self.configure.canvas, (100, 100, 100), (140, y, 110, 14 ) )
                self.gametext.text( row['label'], 80, y, False, False)
                if row['id'] == 'keyboard':
                    text = pygame.key.name(row['key'])
                    self.gametext.text( text, 150, y, False, False)
                elif row['type'] == 'axis' or row['type'] == 'ball' or row['type'] == 'hat':
                    text = row['type'] + " " + str(row['key'])
                    if row['value'] == -1:
                        text += " -"
                    else:
                        text += " +"
                    self.gametext.text( text, 150, y, False, False)
                else:
                    self.gametext.text( row['type'] + " " + str(row['key']), 150, y, False, False)
                y += 15

            # Rumble Support
            pygame.draw.rect(self.configure.canvas, (100, 100, 100), (140, 150, 110, 14 ) )
            self.gametext.text( "Rumble", 80, 150, False, False)
            if rumble_name == False:
                rumble_name = ''
            self.gametext.text( rumble_name, 150, 150, False, False)


            # Draw the menu buttons
            for item in menu_buttons:
                if item.is_visible:
                    item.hover( (mpos_x, mpos_y) ) # check if the mouse is hovering over the button
                    item.draw() # draw the button

            self.configure.display()

        return status

    ''' Audio Configure Screen
        Configuration options for Audio:
            SFX Volume
            Music Volume
        Cancel
        Ok -> Save and go to previous screen
    '''
    def audio(self):
        # Audio options
        print("audio")
