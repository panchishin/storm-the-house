########## IMPORTS ##########

import time
import numpy as np
import sys
import pyautogui
import mss
import cv2
import pykeyboard
import locate
from conf import show_computer_vision, buttons, ammo_upgrade, health_upgrade, basic_upgrades, ammo_bar, state_colors

########## GLOBALS ##########


pyautogui.PAUSE = 0.0 # make mouse clicks instant
keypress = pykeyboard.PyKeyboard() # the keyboard tool
sct = mss.mss() # the screen capture tool

bubble_radius = 80 # area around last click to not click immediately again
sleepy_time = .500 # sleep between frames
ammo_buy = 0 # initial amount of additional ammo to buy

short_sleep = 0.25 # a small amount of time to wait between screen transations and such

upgrade_time = 0.075 # wait time to make sure upgrade clicks get registered

try :
    mon = locate.locate_game()
except :
    print("""Nope!  Doesn't look like you have the window open.
Open a browser, go to http://www.crazygames.com/game/storm-the-house
then get to the start screen of the game.""")
    exit()

previous_state = "initialized"
day = 0


def enter_battle() :
    global sleepy_time, ammo_buy, ammo_bar, bubble_radius, day
    day += 1
    ammo_bar[2] = pic[ammo_bar[1],ammo_bar[0],0]
    bubble_radius = max(10,bubble_radius - 2)
    sleepy_time = max(0,sleepy_time * 0.90 - .01)
    ammo_buy = min(500,int(ammo_buy*1.1+5))
    print("Day",day,", next purchase",ammo_buy,"ammo")


def detect_state(pic):
    global previous_state, state_colors
    colors = tuple(pic[-15,-15])
    color = colors[0]
    if colors in state_colors :
        if state_colors[colors] != previous_state :
            previous_state = state_colors[colors]
            print("Detected state :",previous_state)
            if previous_state == "battle" :
                enter_battle()
            time.sleep(0.1) 
    elif previous_state != "unknown" :
        print("detect_state colors",colors)
        print("Could not find",color,"in states")
        previous_state = "unknown"
    return previous_state


def get_pic():
    global mon
    pic = np.array(sct.grab(mon) ,dtype=np.uint8)
    if mon['width'] != pic.shape[1] :
        return pic[::2,::2,:3]
    else :
        return pic[:,:,:3]

window_initialized = False

def show_pic(pic,wait=1):
    global window_initialized
    if not show_computer_vision:
        return
    if not window_initialized:
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.moveWindow("image", 1000, 0)
        window_initialized = True
    cv2.imshow('image', pic)
    _ = cv2.waitKey(wait)

show_pic(np.zeros([451,599,3]),wait=200)

bubble = []

def in_bubble(i,j):
    global bubble
    for x,y in bubble :
        distance = abs(i-x) + abs(j-y)
        if distance <= bubble_radius :
            return True
    return False

def click(x,y):
    global mon
    pyautogui.click(mon['left']+x,mon['top']+y)

def shoot(pic) :
    global mon, bubble, shooting_area
    
    for x in range(490,0,-3) :
      for y in range(mon['height']-1,int(mon['height']/2),-3) :
        if pic[y][x][0] == 0 and pic[y][x][1] == 0 and pic[y][x][2] == 0:
            if not in_bubble(x,y):
                click(x,y)
                click(x,y) # double tap for the win
                bubble.append((x,y))


if __name__ == "__main__" :

    pic = get_pic()
    show_pic(pic,100)

    while True:
        state = detect_state(pic)

        if state == "start" :
            click(*buttons['play'])
            click(*buttons['play']) # double tap for the win
            time.sleep(short_sleep)

        elif state == "battle" :
            shoot(pic)
            if pic[ammo_bar[1],ammo_bar[0],0] != ammo_bar[2]:
                keypress.press_key(' ')
                time.sleep(.1)
                keypress.release_key(' ')
                time.sleep(.8)
            if sleepy_time >= 0.001 :
                time.sleep(sleepy_time)
            bubble = []

        elif state == "loadout" :
            time.sleep(short_sleep)

            # health upgrade are the most important
            for _ in range(min(int(ammo_buy/2),50)) :
                click(*health_upgrade)
                time.sleep(upgrade_time)

            # try all basic upgrades once
            for upgrade in basic_upgrades :
                click(*upgrade)
                time.sleep(upgrade_time)

            # ammo upgrade 
            for _ in range(int(ammo_buy)) :
                click(*ammo_upgrade)
                time.sleep(upgrade_time)

            # allow the user to quit!
            time.sleep(5)
            click(*buttons['loadout_done'])
            time.sleep(short_sleep)

        elif state == "wait" :
            time.sleep(short_sleep)

        elif state == "retry":
            click(*buttons['retry'])
            click(*buttons['retry']) # double tap for the win
            time.sleep(short_sleep)

     
        else :
            print("Don't have the logic for state'"+state+"' state yet")
            break

        show_pic(pic)
        pic = get_pic()


    print("Exit program")
