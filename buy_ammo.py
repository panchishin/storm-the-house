########## IMPORTS ##########

import time
import numpy as np
import sys
import pyautogui
import mss
import cv2
import pykeyboard
import locate
from conf import ammo_upgrade

########## GLOBALS ##########

ammo_buy = 10 if len(sys.argv) <= 1 else int(sys.argv[1])

pyautogui.PAUSE = 0.0 # make mouse clicks instant
sct = mss.mss() # the screen capture tool

upgrade_time = 0.075 # wait time to make sure upgrade clicks get registered

try :
    mon = locate.locate_game()
except :
    print("""Nope!  Doesn't look like you have the window open.
Open a browser, go to http://www.crazygames.com/game/storm-the-house
then get to the start screen of the game.""")
    exit()


def click(x,y):
    global mon
    pyautogui.click(mon['left']+x,mon['top']+y)


if __name__ == "__main__" :

    # ammo upgrade 
    for _ in range(int(ammo_buy)) :
        click(*ammo_upgrade)
        time.sleep(upgrade_time)
