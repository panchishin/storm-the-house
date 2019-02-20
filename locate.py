import numpy as np
import cv2

from mss import mss
sct = mss()

def show(img,wait=100) :
    cv2.imshow('image', img)
    _ = cv2.waitKey(wait)


def locate_game_using_color(color_val=(72,68,67)):
    mon = sct.monitors[1]
    pic = np.array(sct.grab(mon),dtype=np.uint8)
    scale = int(round(pic.shape[1] / mon['width']))
    if scale > 1 :
        pic = pic[::scale,::scale,:3]
    else :
        pic = pic[:,:,:3]

    a = ( pic[:,:,0] == color_val[0] )
    b = ( pic[:,:,1] == color_val[1] )
    c = ( pic[:,:,2] == color_val[2] )
    e = a * b * c

    locs = np.where( e == True )
    top = locs[0][0]
    bottom = locs[0][-1]
    left = locs[1][0]
    right = locs[1][-1]

    thickness = bottom - top
    height = 940-445
    top = bottom - height

    return {"top": top + mon['top'], "left": left + mon['left'], 'width': 599, 'height': 451}


def locate_game():
    """
    Locates the storm the house in the screen.

    Returns : monitor location : {top,left,width,height}
    """
    try :
        return locate_game_using_color()
    except :
        raise Exception("Cannot find the game on the primary monitor.")


if __name__ == "__main__":
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.moveWindow("image", 1500, 0)

    show(np.zeros((451,599,3), dtype='uint8'),wait=200)

    result = locate_game()

    pic = np.array(sct.grab(result),dtype=np.uint8)
    show(pic)
    print(result)

    _ = cv2.waitKey(5000)