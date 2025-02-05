import cv2
import pyautogui
import mss
import numpy as np
import time
from random import randint


url = "https://www.bettilt618.com/pt"
username = "ThisIsMyUsername"
password = "ThisIsMyPassword"

## 

def clickCoord(pos_click_x,pos_click_y):
    pyautogui.moveTo(pos_click_x, pos_click_y)
    pyautogui.click()
    return

def printSreen(monitor = None):
    
    with mss.mss() as sct:
        if monitor is None:
            monitor = sct.monitors[0]
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}
        sct_img = np.array(sct.grab(monitor))

    # Grab the data 
    return sct_img[:,:,:3]

def positions(target, threshold=0.8,img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def clickImg(img, timeout=3, threshold = 0.7, randomTarget = False ):

    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold)

        if(len(matches)==0):
            has_timed_out = time.time()-start > timeout
            continue
        
        x,y,w,h = matches[0]
        if( randomTarget ):
            matchIdx = randint(0, len(matches)-1)
            x,y,w,h = matches[matchIdx]

        pos_click_x = x+w/2
        pos_click_y = y+h/2
        clickCoord(pos_click_x,pos_click_y)
        return True

    return False

def writeText( sText="" ):
    if len(sText)>0 :
        pyautogui.write( sText )

if __name__ == '__main__': 

    ## Loads image of login stuff
    iniciarSessao = cv2.imread(".\imgs\iniciarSessao.png")
    loginUsername = cv2.imread(".\imgs\loginUsername.png")
    loginPassword = cv2.imread(".\imgs\loginPassword.png")
    loginConfirm = cv2.imread(".\imgs\loginConfirm.png")

    ## Press login button if any
    clickImg( iniciarSessao )
    pyautogui.sleep( 0.2 )
    clickImg( loginUsername )
    writeText( username )
    
    pyautogui.sleep( 0.2 )
    clickImg( loginPassword )
    writeText( password )
    
    pyautogui.sleep( 0.2 )
    clickImg( loginConfirm )

    pass