
# if we should show what the computer sees
show_computer_vision = False

# Relative location of the named buttons
buttons = {
    'play':[468,314],
    'retry':[299,279],
    'loadout_done':[303,413]
    }

# Relative location of each of the upgrades
ammo_upgrade = [63,115]
health_upgrade = [148,114]
basic_upgrades = [ammo_upgrade, health_upgrade, [235,115], [322,116], [408,112]]
all_upgrades = basic_upgrades + [[57,285], [132,286], [210,289]]

# The ammo bar
ammo_bar = [13,32,0]

# Colors for identifying the current state
state_colors = {
    (106, 152, 141) : 'battle',
    (27, 38, 35) : 'loadout' ,
    (19, 8, 202) : 'retry'   ,
    (39, 111, 139) : 'start'   ,
    (225, 235, 232) : 'wait'    ,
    }
