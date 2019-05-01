########## IMPORTS ##########

import time
import sys
import pyautogui

########## GLOBALS ##########

clicks = 50 if len(sys.argv) <= 1 else int(sys.argv[1])
cols = 5 if len(sys.argv) <= 2 else int(sys.argv[2])

pyautogui.PAUSE = 0.02 # make mouse clicks instant

def click(x,y):
    pyautogui.click(x,y)

def position(name):
    print("Locate",name)
    time.sleep(3)
    p = pyautogui.position()
    p = (p.x,p.y)
    print(name,"=",p)
    return p

bug = (880, 538)

collect = [(935, 239), (217, 688), (206, 414), (208, 507), (220, 613), (659, 404), (661, 352) ][:cols]
#collect += [position("another")]

print(collect)


while True:
    for i in range(10) :
        print("round",i)
        for c in collect:
            click(*c)
        #time.sleep(4)
        for _ in range(clicks):
            click(*bug)
    print("sleeping")
    time.sleep(5)