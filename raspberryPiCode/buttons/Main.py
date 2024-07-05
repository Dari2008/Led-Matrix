from buttons.Actions import Actions
from matrix import Variables
import threading
import time
from leds.BackgroundLedStrip import BackgroundLedStrip

def loadLastAnimation():
    if("lastGifPath" not in Variables.LAST_USED_DATA):return
    lastUsedAnimation = Variables.LAST_USED_DATA["lastGifPath"]
    if(lastUsedAnimation != None):
        clear()
        Variables.SERVER.loadGif({
            "name": lastUsedAnimation,
        }, True)

def loadLastPicture():
    ISCLEARING = True
    if("lastImagePath" not in Variables.LAST_USED_DATA):return
    lastUsedPicture = Variables.LAST_USED_DATA["lastImagePath"]
    if(lastUsedPicture != None):
        clear()
        Variables.SERVER.loadImage({
            "name": lastUsedPicture,
        }, True)

def loadLastPlugin():
    if("lastPluginPath" not in Variables.LAST_USED_DATA):return
    lastUsedPlugin = Variables.LAST_USED_DATA["lastPluginPath"]
    if(lastUsedPlugin != None):
        clear()
        Variables.SERVER.loadPlugin({
            "name": lastUsedPlugin,
        }, True)

def clear():
    Variables.MATRIX.clear()
    Variables.MATRIX.show()

SHOWANIMATION = False
POS = 0
ISCLEARING = False

def initLoadingAnimation(color=(255, 255, 0)):
    if(isRunning()):return
    global SHOWANIMATION
    global POS
    POS = 0
    SHOWANIMATION = True
    thread = threading.Thread(target=animate, args=[color], daemon=True)
    thread.start()

def isRunning():
    global SHOWANIMATION
    return SHOWANIMATION

def stopLoadingAnimation():
    global SHOWANIMATION
    global POS
    SHOWANIMATION = False
    POS = 0

def animate(color):
    global SHOWANIMATION
    global POS
    global ISCLEARING

    while SHOWANIMATION:
        if(POS >= 100):
            BackgroundLedStrip.clear()
            BackgroundLedStrip.show()
            return
        
        time.sleep((1/Variables.MATRIX_WIDTH)*0.75)

        leds = getLedsForPos(POS)
        BackgroundLedStrip.clear()
        for led in leds:
            BackgroundLedStrip.setRGBColor(led, color[0], color[1], color[2])

        if(not SHOWANIMATION):
            BackgroundLedStrip.clear()
            BackgroundLedStrip.show()
            return
        BackgroundLedStrip.show()
        POS += 1


def getLedsForPos(pos: int, ) -> list:
    if(pos == 0):
        return []
    if(pos == 100):
        return Variables.LED_STRIP_BOTTOM
    array = (Variables.LED_STRIP_BOTTOM[:int(len(Variables.LED_STRIP_BOTTOM) * (pos / 100))])
    array.reverse()
    return array

def clearDisplay():
    Variables.SERVER.clear(isProgrammatic=True)

isPressed = False

def picturePress():
    global isPressed
    isPressed = True
    initLoadingAnimation()
    initDoubleLoadingBar()

def initDoubleLoadingBar():
    thread = threading.Thread(target=animateDoubleBar, daemon=True)
    thread.start()

def animateDoubleBar():
    global isPressed
    start_time = time.time()
    timeTaken = 0
    wasStopped = False
    while (True):
        timeTaken = time.time() - start_time
        if timeTaken > 2:
            stopLoadingAnimation()
            break
        
        if(timeTaken >= 1 and not wasStopped):
            wasStopped = True
            stopLoadingAnimation()
            initLoadingAnimation((255, 0, 0))

        if(not isPressed):
            break

        time.sleep(0.01)

    stopLoadingAnimation()
    if(timeTaken >= 2):
        clearDisplay()
        isPressed = False
    else:
        loadLastPicture()


def pictureRelease():
    global isPressed
    isPressed = False
    print("Released")
    stopLoadingAnimation()

def run():

    Variables.ACTIONS = Actions()
    
    # Add the actions Clear Screen
    Variables.ACTIONS.addOnPictureBtnPress(picturePress)
    Variables.ACTIONS.addOnPictureBtnRelease(pictureRelease)

    # Add the last used data to the buttons
    Variables.ACTIONS.addOnAnimationBtnHold(loadLastAnimation)
    Variables.ACTIONS.addOnPluginBtnHold(loadLastPlugin)

    Variables.ACTIONS.addOnAnimationBtnPress((lambda: initLoadingAnimation()))
    Variables.ACTIONS.addOnPluginBtnPress((lambda: initLoadingAnimation()))

    Variables.ACTIONS.addOnAnimationBtnRelease(stopLoadingAnimation)
    Variables.ACTIONS.addOnPluginBtnRelease(stopLoadingAnimation)