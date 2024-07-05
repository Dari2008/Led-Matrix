from PIL import Image, ImageEnhance
import matrix.Variables as Variables
from matrix.SettingsManager import SettingsManager
from leds.BackgroundLedStrip import BackgroundLedStrip
import json
import os

class ImageLoader:

    @staticmethod
    def displayImage(name) -> json:
        path = Variables.IMAGE_DIR + name

        width = Variables.MATRIX_WIDTH
        height = Variables.MATRIX_HEIGHT


        try:
            img = Image.open(path)
            imgwidth = img.width
            imgheight = img.height

            xoffset = 0
            yoffset = 0

            settings = SettingsManager.getImageSettings(name)

            paddingX = "center"
            paddingY = "center"

            customWidth = imgwidth
            customHeight = imgheight

            customXOffset = 0
            customYOffset = 0

            brightness = 1
            bgBrightness = 1

            backgroundLedStripMethod = settings["backgroundLedStripMethod"] if "backgroundLedStripMethod" in settings else "none"

            if "paddingX" in settings:
                paddingX = settings["paddingX"]

            if "paddingY" in settings:
                paddingY = settings["paddingY"]

            if "width" in settings:
                customWidth = settings["width"]

            if "height" in settings:
                customHeight = settings["height"]

            if "xOffset" in settings:
                customXOffset = settings["xOffset"]

            if "yOffset" in settings:
                customYOffset = settings["yOffset"]

            if "brightness" in settings:
                brightness = settings["brightness"] / 100

            if "bgBrightness" in settings:
                bgBrightness = settings["bgBrightness"] / 100

            if customWidth != imgwidth or customHeight != imgheight:
                img = ImageLoader.resizeImage(img, customWidth, customHeight, settings)
                imgwidth = img.width
                imgheight = img.height


            if paddingX == "left":
                xoffset = 0
            elif paddingX == "right":
                xoffset = width - imgwidth
            elif paddingX == "center":
                xoffset = (width - imgwidth) / 2

            if paddingY == "top":
                yoffset = 0
            elif paddingY == "bottom":
                yoffset = height - imgheight
            elif paddingY == "center":
                yoffset = (height - imgheight) / 2

            yoffset = int(yoffset)
            xoffset = int(xoffset)

            xoffset += customXOffset
            yoffset += customYOffset

            BackgroundLedStrip.setColorsFromImage(backgroundLedStripMethod, img, xoffset, yoffset, bgBrightness)

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)

            Variables.MATRIX.drawImage(img, xoffset, yoffset)
            Variables.MATRIX.show()
            ImageLoader.IS_IMAGE_SHOWN = True
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while loading image", "e": e}
        
    @staticmethod
    def hideImage():
        ImageLoader.IS_IMAGE_SHOWN = False
        Variables.MATRIX.createNewImage()
        Variables.MATRIX.show()
        return {"ok": True}
    
    @staticmethod
    def isActive():
        return ImageLoader.IS_IMAGE_SHOWN
    
    @staticmethod
    def removeImage(name):
        try:
            SettingsManager.removeImageSettings(name)
            return {"ok": True, "returnCode": os.system(f"rm {Variables.IMAGE_DIR + name} -f")}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while removing image", "e": e}
        
    @staticmethod
    def getImages():
        data = []
        for name in os.listdir(Variables.IMAGE_DIR):
            if name == "__pycache__":
                continue
            try:
                size = Image.open(Variables.IMAGE_DIR + name).size
                settings = SettingsManager.getImageSettings(name)
                data.append({
                    "name": name, 
                    "uploaded": os.path.getctime(Variables.IMAGE_DIR + name), 
                    "dimensions": {
                        "width": ImageLoader.getOrDefault(settings, "width", size[0]), 
                        "height": ImageLoader.getOrDefault(settings, "height", size[1])
                    },
                    "width": ImageLoader.getOrDefault(settings, "width", size[0]), 
                    "height": ImageLoader.getOrDefault(settings, "height", size[1]),
                    "settings": settings
                })
            except Exception as e:
                print(e)
                data.append({
                    "name": name, 
                    "uploaded": os.path.getctime(Variables.IMAGE_DIR + name), 
                    "dimensions": "Error while loading image dimensions", 
                    "exception": e.__str__()
                })

        return data
    
    @staticmethod
    def getOrDefault(settings, key, value):
        if key in settings:
            return settings[key]
        return value
    
    @staticmethod
    def resizeImage(img, width, height, settings):
        resizeMethod = None
        if "resizeMethod" in settings:
            resizeMethod = getattr(Image.Resampling, settings["resizeMethod"], None)
        return img.resize((width, height), resample=resizeMethod)

    IS_IMAGE_SHOWN = False
