import json
from PIL import Image, ImageSequence, ImageEnhance, ImageFont
import math
import matrix.Variables as Variables
import time
import os
from fonts.FontLoader import FontLoader

from matrix.SettingsManager import SettingsManager
from matrix.KillableThread import KillableThread
from leds.BackgroundLedStrip import BackgroundLedStrip

class GifLoader:

    @staticmethod
    def displayGif(name) -> json:
        path = Variables.GIF_DIR + name
        try:
            gif = Image.open(path)
            GifLoader.CURRENT_ANIMATION_THREAD = KillableThread(target=GifLoader.loadGif, args=(gif, name))
            GifLoader.CURRENT_ANIMATION_THREAD_RUNNING = True
            GifLoader.CURRENT_ANIMATION_THREAD.start()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "msg": "Error while loading gif", "e": e}
        
    @staticmethod
    def hideGif():
        GifLoader.CURRENT_ANIMATION_THREAD_RUNNING = False
        if(GifLoader.CURRENT_ANIMATION_THREAD != None):
            GifLoader.CURRENT_ANIMATION_THREAD.kill()
            return {"ok": True}
        return {"ok": False, "msg": "No gif loaded"}
        
    @staticmethod
    def loadGif(gif: Image, name:str):
        currentCount = 0
        fdelay = -1
        speedMultiplyer = 1
        count = -1
        infinite = False
        backgroundImageMethodTiming = "everyFrame"
        backgroundLedStripMethod = "none"

        settings = SettingsManager.getGifSettings(name)

        if("count" in settings):
            count = settings["count"]

        if("fdelay" in settings):
            fdelay = settings["fdelay"]

        if("speedMultiplyer" in settings):
            speedMultiplyer = settings["speedMultiplyer"]

        if("inifinityLoop" in settings):
            infinite = settings["inifinityLoop"]
            
        if("backgroundImageMethodTiming" in settings):
            backgroundImageMethodTiming = settings["backgroundImageMethodTiming"]

        if("backgroundLedStripMethod" in settings):
            backgroundLedStripMethod = settings["backgroundLedStripMethod"]

        images = []

        images = GifLoader.processImages(gif, settings, backgroundImageMethodTiming, backgroundLedStripMethod)

        startDisplayTime = time.time()

        if(backgroundImageMethodTiming == "firstFrame" and len(images) > 0):
            BackgroundLedStrip.setColorsFromImage(backgroundLedStripMethod, images[0]["image"], 0, 0)


        while GifLoader.CURRENT_ANIMATION_THREAD_RUNNING:
            for i in range(0, len(images)):
                if(not GifLoader.CURRENT_ANIMATION_THREAD_RUNNING):return

                currentImage = images[i]
                Variables.MATRIX.setImage(currentImage["image"])
                Variables.MATRIX.show()

                if(backgroundImageMethodTiming == "everyFrame"):
                    if "leds" in currentImage:
                        BackgroundLedStrip.setLeds(currentImage["leds"])
                        BackgroundLedStrip.show()

                duration = 100

                if ("duration" in currentImage["info"]):
                    duration = currentImage["info"]["duration"]
                
                if(fdelay != -1 and fdelay != None):
                    duration = fdelay

                duration = duration * speedMultiplyer

                currentTime = time.time()
                timePassed = (currentTime - startDisplayTime)

                if(duration / 1000 - timePassed > 0):
                    time.sleep(abs(duration / 1000 - timePassed))

                startDisplayTime = time.time()

            if(count!=-1 and not infinite):currentCount += 1
            if(not GifLoader.CURRENT_ANIMATION_THREAD_RUNNING):return

            if(currentCount >= count and not infinite):
                GifLoader.CURRENT_ANIMATION_THREAD_RUNNING = False
                break

            if(not infinite and currentCount >= count):
                GifLoader.CURRENT_ANIMATION_THREAD_RUNNING = False
                break

        Variables.SERVER.clear()

    @staticmethod
    def processImages(gif: Image.Image, settings, backgroundImageMethodTiming, backgroundLedStripMethod):
        images = []
        customWidth = -1
        customHeight = -1
        xoffset = 0
        yoffset = 0
        paddingX = "center"
        paddingY = "center"
        customXOffset = 0
        customYOffset = 0
        brightness = 1
        bgBrightness = 1
        imgs = 0 

        for frame in ImageSequence.Iterator(gif):
            imgs += 1

        percentPerImage = 100 / imgs

        if "paddingX" in settings:
            paddingX = settings["paddingX"]
        if "paddingY" in settings:
            paddingY = settings["paddingY"]

        if "xOffset" in settings:
            customXOffset = settings["xOffset"]
        if "yOffset" in settings:
            customYOffset = settings["yOffset"]
            
        if("brightness" in settings):
            brightness = settings["brightness"] / 100

        if("bgBrightness" in settings):
            bgBrightness = settings["bgBrightness"] / 100

        def getXOffset(alignX, width, customXOffset = 0):
            if alignX == "left":
                return customXOffset
            elif alignX == "right":
                return Variables.MATRIX_WIDTH - width + customXOffset
            elif alignX == "center":
                return (Variables.MATRIX_WIDTH - width) / 2 + customXOffset
            else:
                return customXOffset
            
        def getYOffset(alignY, height, customYOffset = 0):
            if alignY == "top":
                return customYOffset
            elif alignY == "bottom":
                return Variables.MATRIX_HEIGHT - height + customYOffset
            elif alignY == "center":
                return (Variables.MATRIX_HEIGHT - height) / 2 + customYOffset
            else:
                return customYOffset

        resizseMethod = None
        if "width" in settings:
            customWidth = settings["width"]
        if "height" in settings:
            customHeight = settings["height"]
        if "resizseMethod" in settings:
            resizseMethod = getattr(Image.Resampling, settings["resizseMethod"])

        for frame in ImageSequence.Iterator(gif):

            if customWidth != -1 or customHeight != -1:
                if customWidth == -1:
                    customWidth = frame.width
                if customHeight == -1:
                    customHeight = frame.height
                frame = frame.resize((customWidth, customHeight), resample=resizseMethod)

            xoffset = int(getXOffset(paddingX, frame.width, customXOffset))
            yoffset = int(getYOffset(paddingY, frame.height, customYOffset))

            newFullSize128By64Image = Image.new("RGB", (Variables.MATRIX_WIDTH, Variables.MATRIX_HEIGHT))

            if(gif.mode != "RGB"):
                tmpImage2 = Image.new("RGBA", (frame.width, frame.height), (0, 0, 0, 255))
                tmpImage = Image.alpha_composite(tmpImage2, frame)
                newFullSize128By64Image.paste(tmpImage, (xoffset, yoffset))
            else:
                newFullSize128By64Image.paste(frame, (xoffset, yoffset))

            newFullSize128By64Image = ImageEnhance.Brightness(newFullSize128By64Image).enhance(brightness)
            
            if backgroundImageMethodTiming != "firstFrame":
                images.append({
                    "image": newFullSize128By64Image, 
                    "leds":BackgroundLedStrip.getColorsFromImage(backgroundLedStripMethod, newFullSize128By64Image, 0, 0, bgBrightness), 
                    "info": gif.info
                })
            else:
                images.append({
                    "image": newFullSize128By64Image, 
                    "info": gif.info
                })

        return images
    
    @staticmethod
    def isActive():
        return GifLoader.CURRENT_ANIMATION_THREAD_RUNNING
    
    @staticmethod
    def removeGif(name):
        try:
            SettingsManager.removeGifSettings(name)
            return {"ok": True, "returnCode": os.system("rm " + Variables.GIF_DIR + name + " -f")}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while removing image", "e": e}
        
    @staticmethod
    def getGifs():
        data = []
        for name in os.listdir(Variables.GIF_DIR):
            if name == "__pycache__":
                continue
            
            try:
                settings = SettingsManager.getGifSettings(name)
                data.append({
                    "name": name, 
                    "uploaded": os.path.getctime(Variables.GIF_DIR + name), 
                    "frameCount": Image.open(Variables.GIF_DIR + name).n_frames, 
                    "frameDelay": GifLoader.getOrDefault(settings, "fdelay", Image.open(Variables.GIF_DIR + name).info["duration"]),
                    "width": GifLoader.getOrDefault(settings, "width", Image.open(Variables.GIF_DIR + name).width),
                    "height": GifLoader.getOrDefault(settings, "height", Image.open(Variables.GIF_DIR + name).height),
                    "settings": settings
                    })
            except Exception as e:
                print(e)
                data.append({
                    "name": name, 
                    "uploaded": os.path.getctime(Variables.GIF_DIR + name), 
                    "error": "Error while loading gif info", 
                    "exception": e.__str__()
                    })

        return data
    
    @staticmethod
    def getOrDefault(settings, key, other):
        if key in settings:
            return settings[key]
        return other
    

    CURRENT_ANIMATION_THREAD = None
    CURRENT_ANIMATION_THREAD_RUNNING = False
