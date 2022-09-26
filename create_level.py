import json

'''
All this file does is make it easy to manually write scripts which save 
to a level file which is read by the game
'''

level_data = { 
    # Level entry, in space
    1: { 'name': "STARFIELD", 'speed': 'fast' },
    2: { 'name': "FADE", 'value': 255, 'color': (0,0,0)},


    100: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
    150: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
    200: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
    250: { 'name': "ENEMY", 'type': 11, 'x': 320, 'y': 50 },

    251: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 50, 'powerup': 4 },


    300: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
    350: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
    400: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
    450: { 'name': "ENEMY", 'type': 11, 'x': 320, 'y': 150 },

    451: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 100, 'powerup': 4 },

    452: { 'name': "STARFIELD", 'speed': 'slow' },

    510: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 50 },
    530: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 100 },
    550: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 150 },
    570: { 'name': "ENEMY", 'type': 10, 'x': 320, 'y': 200 },

    600: { 'name': "ENEMY", 'type': 13, 'x': 320, 'y': 70 },
    601: { 'name': "ENEMY", 'type': 13, 'x': 320, 'y': 130 },
    602: { 'name': "STARFIELD", 'speed': 'none' },
    603: { 'name': "BACKGROUND", 'file':'assets/Images/background.png'},
    604: { 'name': "FADE", 'value': 0, 'color': (0,0,0)},

    # Landscape intro here
    700: { 'name': "OBJECT", 'file':'assets/Images/ceiling.png', 'width':320, 'height':40, 'x':320, 'y':-40, 'collide':True, 'scroll':'left', 'scroll_speed': 2, 'scroll_repeat': True},
    701: { 'name': "OBJECT", 'file':'assets/Images/ground.png', 'width':320, 'height':40, 'x':320, 'y':240, 'collide':True, 'scroll':'left', 'scroll_speed': 1, 'scroll_repeat': True},

    # In cave
    801: { 'name': "DARKNESS" },

    # mini-boss enemy pattern
    1001: { 'name': "BRIGHTNESS" }, # lol?
    1000: { 'name': "ENEMY", 'type': 13, 'x': 320, 'y': 70 },
    1010: { 'name': "ENEMY", 'type': 13, 'x': 320, 'y': 100 },
    1020: { 'name': "ENEMY", 'type': 13, 'x': 320, 'y': 130 },
    1030: { 'name': "ENEMY", 'type': 13, 'x': 320, 'y': 160 },

    # flash red boss alert
    2000: { 'name': "NUKE" },
    2001: { 'name': "BACKGROUND", 'file':'none'},
    2002: { 'name': "FADE", 'value': 0, 'color': (0,0,0)},
    2102: { 'name': "FADE", 'value': 255, 'color': (255,0,0)},
    2152: { 'name': "FADE", 'value': 0, 'color': (255,0,0)},
    2202: { 'name': "FADE", 'value': 255, 'color': (255,0,0)},
    2252: { 'name': "FADE", 'value': 0, 'color': (255,0,0)},

    2300: { 'name': "BOSS", 'type': 1}, # boss #1 yay
    2500: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 100 },
    3000: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 50 },
    3500: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 200 },
    4000: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 150 },
    4500: { 'name': "ENEMY", 'type': 12, 'x': 320, 'y': 100 },


}

# Save Level
level_json = json.dumps(level_data)
file = open('assets/Levels/earth.level', 'w')
file.write(level_json)
file.close()

'''
# Load Level
with open('assets/Levels/earth.level') as readfile:
    self.script = json.load(readfile)
'''
