########## IMPORTS ##########

import time
import numpy as np
import sys
import pyautogui
import mss
import cv2
import pykeyboard
import locate
from conf import show_computer_vision, buttons, upgrades, ammo, state_colors

########## GLOBALS ##########


pyautogui.PAUSE = 0.0 # make mouse clicks instant
keypress = pykeyboard.PyKeyboard() # the keyboard tool
sct = mss.mss() # the screen capture tool

bubble_radius = 80 # area around last click to not click immediately again
sleepy_time = .500 # sleep between frames
ammo_buy = 0 # initial amount of additional ammo to buy

short_sleep = 0.25 # a small amount of time to wait between screen transations and such

try :
    mon = locate.locate_game()
except :
    print("""Nope!  Doesn't look like you have the window open.
Open a browser, go to http://www.crazygames.com/game/storm-the-house
then get to the start screen of the game.""")
    exit()

previous_state = "initialized"

def detect_state(pic):
    global previous_state, state_colors, sleepy_time, ammo_buy, ammo, bubble_radius
    colors = tuple(pic[-15,-15])
    color = colors[0]
    if colors in state_colors :
        if state_colors[colors] != previous_state :
            print("detect_state colors",colors)
            previous_state = state_colors[colors]
            print("Found new state :",previous_state)
            if previous_state == "battle" :
                ammo[2] = pic[ammo[1],ammo[0],0]
                bubble_radius = max(35,bubble_radius - 5)
                sleepy_time = max(0,sleepy_time * 0.90 - .01)
                ammo_buy = min(200,ammo_buy+5)
                print("Sleepy time",int(1000*sleepy_time),"ms, ammo buy",ammo_buy)
            time.sleep(0.1) 
    elif previous_state != "unknown" :
        print("detect_state colors",colors)
        print("Could not find",color,"in states")
        previous_state = "unknown"
    return previous_state


########## SET UP CV2 WINDOW ##########



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
                click(x,y)
                bubble.append((x,y))


if __name__ == "__main__" :

    pic = get_pic()
    show_pic(pic,100)

    while True:
        state = detect_state(pic)

        if state == "start" :
            click(*buttons['play'])
            click(*buttons['play'])
            time.sleep(short_sleep)

        elif state == "battle" :
            shoot(pic)
            if pic[ammo[1],ammo[0],0] != ammo[2]:
                keypress.press_key(' ')
                time.sleep(.1)
                keypress.release_key(' ')
                time.sleep(.8)
                bubble = []
            if sleepy_time >= 0.001 :
                bubble = bubble[-6:][1:]
                time.sleep(sleepy_time)
            else :
                bubble = []

        elif state == "loadout" :
            time.sleep(short_sleep)
            for _ in range(min(20,max(0,int(ammo_buy/10)-5))) :
                for upgrade in upgrades:
                    click(*upgrade)
                    time.sleep(0.1)
            for _ in range(int(ammo_buy)) :
                click(*upgrades[0]) # bullets
                time.sleep(0.1)
                click(*upgrades[1]) # health
                time.sleep(0.1)
            time.sleep(5)
            click(*buttons['loadout_done'])
            time.sleep(short_sleep)

        elif state == "wait" :
            time.sleep(short_sleep)

        elif state == "retry":
            click(*buttons['retry'])
            click(*buttons['retry'])
            time.sleep(short_sleep)

     
        else :
            print("Don't have the logic for state'"+state+"' state yet")
            break

        show_pic(pic)
        pic = get_pic()


    print("Exit program")
