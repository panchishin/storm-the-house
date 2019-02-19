########## IMPORTS ##########

import time
import numpy as np
import sys
import pyautogui
import mss
import cv2
import pykeyboard
import locate
from storm_the_house import get_pic, show_pic, detect_state

sct = mss.mss() # the screen capture tool

mon = locate.locate_game()

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.moveWindow("image", 1000, 0)

show_pic(np.zeros([451,599,4]),wait=200)

pic = get_pic()
show_pic(pic,100)

state = detect_state(pic)
print("go to the location")
for _ in range(6):
    time.sleep(3)
    p = pyautogui.position()
    print("dx,dy ["+str(p.x-mon['left'])+","+str(p.y-mon['top'])+"]")
exit()
