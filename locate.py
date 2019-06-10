import numpy as np
import cv2

from mss import mss
sct = mss()

def show(img,wait=100) :
    cv2.imshow('image', img)
    _ = cv2.waitKey(wait)


def locate_game_using_color(monitor=1,color_val=(62,152,203)):  # this is the orange color of intro screen.
    mon = sct.monitors[monitor]
    pic = np.array(sct.grab(mon),dtype=np.uint8)
    scale = int(round(pic.shape[1] / mon['width']))
    print(f"The scale is {scale}")
    if scale > 1 :
        pic = pic[::scale,::scale,:3]
    else :
        pic = pic[:,:,:3]

    a = ( pic[:,:,0] == color_val[0] )
    b = ( pic[:,:,1] == color_val[1] )
    c = ( pic[:,:,2] == color_val[2] )
    e = a * b * c

    locs = np.where( e == True )
    return {'top':locs[0].min(),'left':locs[1].min(),'height':451,'width':599}


def locate_game():
    """
    Locates the storm the house in the screen.

    Returns : monitor location : {top,left,width,height}
    """
    try :
        for monitor in range(len(sct.monitors)) :
            if sct.monitors[monitor]['top'] == 0 :
                return locate_game_using_color(monitor=monitor)
            else :
                print(f"Can't use monitor {monitor}, not primary")
    except :
        raise Exception("Cannot find the game on the primary monitor.  Try moving the game window to another monitor.")


if __name__ == "__main__":
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.moveWindow("image", 1000, 0)

    show(np.zeros((451,599,3), dtype='uint8'),wait=200)

    result = locate_game()

    pic = np.array(sct.grab(result),dtype=np.uint8)
    print("the color at the top left is ",pic[0,0])
    show(pic,wait=2000)
    print(result)

    _ = cv2.waitKey(5000)