import pygame

# ----- Import from other files ----

# ----- Classes -----
''' Controls
    Handles all input from Keyboard and/or Joysticks

'''
class Controls(object):

    def __init__(self, configure):

        self.configure = configure

        self.joystick_num = pygame.joystick.get_count()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(self.joystick_num)]

        for x in range(self.joystick_num):
            joystick = pygame.joystick.Joystick(x)
            joystick.init()

            print("Instance:", joystick.get_instance_id())
            print("Guid:", joystick.get_guid())
            print("Name:", joystick.get_name())

    ''' Wait for Key
        Waits for a key (or joystick button) to be pressed
    '''
    def wait_for_key(self):
        status = []
        while len(status) == 0:
            status = self.get_key()

        return status[0]

    # get_key_pressed(self):  # Return all keys being pressed (polling states)
    def get_key_pressed(self):
        status_list = []
        key = pygame.key.get_pressed() # Grab all polling states for keyboard
        for row in self.configure.control_map:

            status = {'label':'', 'key':False, 'id':'', 'type':'', 'value':''} # default values (nothing being "pressed")

            # keyboard values
            if row['id'] == 'keyboard':
                status = row.copy()
                status['value'] = key[row['key']]

            # joystick values
            for x in range(self.joystick_num):
                joystick = pygame.joystick.Joystick(x)

                if row['id'] == joystick.get_guid():

                    if row['type'] == 'button':
                        status = row.copy()
                        status['value'] = joystick.get_button(row['key'])
                    elif row['type'] == 'axis' or row['type'] == 'ball' or row['type'] == 'hat':
                        status = row.copy()
                        if status['value'] == 1: # key mapping, axis: key=0, value= -1 (left) or +1 (right)
                            if joystick.get_axis(row['key']) > 0.1:
                                status['value'] = True
                            else:
                                status['value'] = False
                        elif status['value'] == -1: # key mapping, axis: key=0, value= -1 (left) or +1 (right)
                            if joystick.get_axis(row['key']) < -0.1:
                                status['value'] = True
                            else:
                                status['value'] = False

            status_list.append(status)

        return status_list


    ''' Get Key
        go through events and return the key status stuff
        (should return ALL events, right now it just returns ONE)
    '''
    def get_key(self):
        status_list = []
        for event in pygame.event.get():
            status = {'label':'', 'key':-1, 'id':'', 'type':'', 'value':''} # default values (nothing being "pressed")
            if event.type == pygame.QUIT:
                key = 'exit'
                status['label'] = 'QUIT'
                status['key'] = 'QUIT'
                status['id'] = 'SYSTEM'
                status['type'] = 'click'
                status['value'] = 'x'
            # Keyboard
            if event.type == pygame.KEYDOWN:
                status['key'] = event.key
                status['id'] = 'keyboard'
                status['type'] = 'key'
                status['value'] = event.key
            # Joystick
            if event.type == pygame.JOYBUTTONDOWN:
                for x in range(self.joystick_num):
                    joystick = pygame.joystick.Joystick(x)
                    if joystick.get_button(event.button):
                        status['id'] = joystick.get_guid()
                        status['key'] = event.button
                        status['type'] = 'button'
                        status['value'] = '1'
            if event.type == pygame.JOYAXISMOTION and (event.value < -0.1 or event.value > 0.1):
                for x in range(self.joystick_num):
                    joystick = pygame.joystick.Joystick(x)
                    if joystick.get_axis(event.axis):
                        status['id'] = joystick.get_guid()
                        status['key'] = event.axis
                        status['type'] = 'axis'
                        if event.value < 0:
                            status['value'] = -1
                        else:
                            status['value'] = 1
            if event.type == pygame.JOYBALLMOTION:
                for x in range(self.joystick_num):
                    joystick = pygame.joystick.Joystick(x)
                    if joystick.get_axis(event.ball) and (event.value < -0.1 or event.value > 0.1):
                        status['id'] = joystick.get_guid()
                        status['key'] = event.ball
                        status['type'] = 'ball'
                        status['value'] = event.value
            if event.type == pygame.JOYHATMOTION and (event.value < -0.1 or event.value > 0.1):
                for x in range(self.joystick_num):
                    joystick = pygame.joystick.Joystick(x)
                    if joystick.get_axis(event.hat):
                        status['id'] = joystick.get_guid()
                        status['key'] = event.hat
                        status['type'] = 'hat'
                        status['value'] = event.value

            if status['key'] != -1:
                for row in self.configure.control_map:
                    if status['key'] == row['key'] and status['id'] == row['id'] and status['type'] == row['type']:
                        status['label'] = row['label'] # found a matching control map 
                status_list.append(status)


        return status_list

    def rumble(self, controller_id, duration): # Python 2.0.2
        for x in range(self.joystick_num):
            joystick = pygame.joystick.Joystick(x)

            if joystick.get_guid() == controller_id:
                joystick.rumble(0, 1, duration) # Low, High, Time (ms); returns False if not supported

    def get_name(self, controller_id):
        for x in range(self.joystick_num):
            joystick = pygame.joystick.Joystick(x)

            return joystick.get_name()
        return False