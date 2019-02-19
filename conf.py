
# if we should show what the computer sees
show_computer_vision = False

# Relative location of the named buttons
buttons = {
    'play':[468,314],
    'retry':[299,279],
    'loadout_done':[303,413]
    }

# Relative location of each of the upgrades
upgrades = [[63,115], [148,114], [235,115], [322,116], [408,112], [57,285], [132,286], [210,289]]

# The ammo bar
ammo = [13,32,0]

# Colors for identifying the current state
state_colors = {
    (106, 152, 141, 255) : 'battle',
    (27, 38, 35, 255) : 'loadout' ,
    (19, 8, 202, 255) : 'retry'   ,
    (39, 111, 139, 255) : 'start'   ,
    (225, 235, 232, 255) : 'wait'    ,
    }
