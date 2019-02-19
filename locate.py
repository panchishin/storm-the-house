import numpy as np
import cv2

from mss import mss
sct = mss()

def show(img,wait=100) :
    cv2.imshow('image', img)
    _ = cv2.waitKey(wait)

def locate_game_on_monitor(monitor_number=1):
    color_val=[63,60,59,255]
    mon = sct.monitors[monitor_number]
    pic = np.array(sct.grab(mon),dtype=np.uint8)
    scale = int(round(pic.shape[1] / mon['width']))
    if scale > 1 :
        pic = pic[::scale,::scale,:]
        color_val = [ 72,  68,  67, 255]

    a = ( pic[:,:,0] == color_val[0] )
    b = ( pic[:,:,1] == color_val[1] )
    c = ( pic[:,:,2] == color_val[2] )
    d = ( pic[:,:,3] == color_val[3] )
    e = a * b * c * d

    locs = np.where( e == True )
    top = locs[0][0]
    bottom = locs[0][-1]
    left = locs[1][0]
    right = locs[1][-1]

    thickness = bottom - top
    height = 940-445
    top = bottom - height
    bottom -= thickness

    result = {"top": top + mon['top'], "left": left + mon['left'], "width": right-left, "height": bottom-top}

    return result

def locate_game():
    """
    Locates the storm the house in the screen.

    Returns : monitor location : {top,left,width,height}
    """
    for monitor in range(1,5):
        try :
            return locate_game_on_monitor(monitor)
        except :
            pass
    raise """Cannot find the game window in any monitor."""


if __name__ == "__main__":
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.moveWindow("image", 1500, 0)

    show(np.zeros([451,599,4], dtype='uint8'),wait=200)

    result = locate_game()

    pic = np.array(sct.grab(result),dtype=np.uint8)
    show(pic)
    print(result)

    _ = cv2.waitKey(5000)