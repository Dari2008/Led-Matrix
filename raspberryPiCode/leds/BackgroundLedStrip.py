import matrix.Variables as Variables
from rpi_ws281x import PixelStrip, Color, ws
from leds.SystemUtils import SystemUtils
import time
import PIL.Image as Image
from other.AutomatedDisplayShutdown import AutomatedDisplayShutdown

class BackgroundLedStrip:

    @staticmethod
    def setColorsFromImage(backgroundLedStripSetting, img, xoffset, yoffset, brightness):
        BackgroundLedStrip.tmpLeds = BackgroundLedStrip.getColorsFromImage(backgroundLedStripSetting, img, xoffset, yoffset, brightness)
        BackgroundLedStrip.show()

    @staticmethod
    def getColorsFromImage(backgroundLedStripSetting, img, xoffset, yoffset, brightness):
        if backgroundLedStripSetting == "none":
            return [Color(0, 0, 0) for _ in range(BackgroundLedStrip.numPixels())]
        elif backgroundLedStripSetting == "averageColor":
            return BackgroundLedStrip.setAverageColor(img, brightness)
        elif backgroundLedStripSetting == "averageColorLines":
            return BackgroundLedStrip.setAverageColorLines(img, xoffset, yoffset, brightness)
        elif backgroundLedStripSetting == "outerRing":
            return BackgroundLedStrip.setOuterRing(img, xoffset, yoffset, brightness)
    
    @staticmethod
    def setAverageColor(img, brightness):
        img = img.resize((1, 1))
        r, g, b = img.getpixel((0, 0))
        color = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)
        return [color for _ in range(BackgroundLedStrip.numPixels())]

    @staticmethod
    def setAverageColorLines(img, xoffset, yoffset, brightness):
        newFullSizeImage = Image.new("RGB", (Variables.MATRIX_WIDTH, Variables.MATRIX_HEIGHT))
        newFullSizeImage.paste(img, (xoffset, yoffset))
        img = newFullSizeImage
        leds = [Color(0, 0, 0) for _ in range(BackgroundLedStrip.numPixels())]

        isFirstLeft = True
        isFirstTop = True

        if not (len(Variables.LED_STRIP_LEFT) >= len(Variables.LED_STRIP_RIGHT)):
            isFirstLeft = False

        if not (len(Variables.LED_STRIP_TOP) >= len(Variables.LED_STRIP_BOTTOM)):
            isFirstTop = False

        # Left and right
        imgHor = img.resize( (1, len(Variables.LED_STRIP_LEFT)) if isFirstLeft else (1, len(Variables.LED_STRIP_RIGHT)))
        for y in range(0, len(Variables.LED_STRIP_LEFT) if isFirstLeft else len(Variables.LED_STRIP_RIGHT)):
            r, g, b = imgHor.getpixel((0, y))
            leds[Variables.LED_STRIP_LEFT[y] if isFirstLeft else Variables.LED_STRIP_RIGHT[y]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)
                

        imgHor = imgHor.resize( (1, len(Variables.LED_STRIP_LEFT)) if not isFirstLeft else (1, len(Variables.LED_STRIP_RIGHT)))
        for y in range(0, len(Variables.LED_STRIP_LEFT) if not isFirstLeft else len(Variables.LED_STRIP_RIGHT)):
            r, g, b = imgHor.getpixel((0, y))
            leds[Variables.LED_STRIP_LEFT[y] if not isFirstLeft else Variables.LED_STRIP_RIGHT[y]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)


        # Top and bottom
        imgVert = img.resize((len(Variables.LED_STRIP_TOP), 1) if isFirstTop else (len(Variables.LED_STRIP_BOTTOM), 1))
        for x in range(0, len(Variables.LED_STRIP_TOP) if isFirstTop else len(Variables.LED_STRIP_BOTTOM)):
            r, g, b = imgVert.getpixel((x, 0))
            leds[Variables.LED_STRIP_TOP[x] if isFirstTop else Variables.LED_STRIP_BOTTOM[x]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)

                
        imgVert = imgVert.resize((len(Variables.LED_STRIP_TOP), 1) if not isFirstTop else (len(Variables.LED_STRIP_BOTTOM), 1))
        for x in range(0, len(Variables.LED_STRIP_TOP) if not isFirstTop else len(Variables.LED_STRIP_BOTTOM)):
            r, g, b = imgVert.getpixel((x, 0))
            leds[Variables.LED_STRIP_TOP[x] if not isFirstTop else Variables.LED_STRIP_BOTTOM[x]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)

        return leds
    
    @staticmethod
    def getColorWithAlpha(color, alpha):
        return Color(int(color.r * alpha), int(color.g * alpha), int(color.b * alpha))

    @staticmethod
    def setOuterRing(img, xoffset, yoffset, brightness):

        newFullSizeImage = Image.new("RGB", (Variables.MATRIX_WIDTH, Variables.MATRIX_HEIGHT))
        newFullSizeImage.paste(img, (xoffset, yoffset))

        img = newFullSizeImage.resize((len(Variables.LED_STRIP_TOP), len(Variables.LED_STRIP_LEFT)))
        img2 = newFullSizeImage.resize((len(Variables.LED_STRIP_BOTTOM), len(Variables.LED_STRIP_RIGHT)))

        leds = [Color(0, 0, 0) for _ in range(BackgroundLedStrip.numPixels())]

        for y in range(0, len(Variables.LED_STRIP_LEFT)):
            r, g, b = img.getpixel((0, y))
            leds[Variables.LED_STRIP_LEFT[y]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)
            # BackgroundLedStrip.setColor(Variables.LED_STRIP_LEFT[y], Color(r, g, b))

        for y in range(0, len(Variables.LED_STRIP_RIGHT)):
            r, g, b = img2.getpixel((len(Variables.LED_STRIP_BOTTOM) - 1, y))
            leds[Variables.LED_STRIP_RIGHT[y]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)
            # BackgroundLedStrip.setColor(Variables.LED_STRIP_RIGHT[y], Color(r, g, b))

        for x in range(0, len(Variables.LED_STRIP_TOP)):
            r, g, b = img.getpixel((x, 0))
            leds[Variables.LED_STRIP_TOP[x]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)
            # BackgroundLedStrip.setColor(Variables.LED_STRIP_TOP[x], Color(r, g, b))

        for x in range(0, len(Variables.LED_STRIP_BOTTOM)):
            r, g, b = img2.getpixel((x, len(Variables.LED_STRIP_RIGHT) - 1))
            leds[Variables.LED_STRIP_BOTTOM[x]] = BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness)
            # BackgroundLedStrip.setColor(Variables.LED_STRIP_BOTTOM[x], Color(r, g, b))

        return leds

    @staticmethod
    def setLeds(leds):
        BackgroundLedStrip.tmpLeds = leds

    @staticmethod
    def getLeds():
        return BackgroundLedStrip.tmpLeds
    
    @staticmethod
    def setEntireColor(color):
        BackgroundLedStrip.tmpLeds = [color for _ in range(BackgroundLedStrip.numPixels())]

    @staticmethod
    def getColorForUsage(val) -> Color:
        green = (0, 255, 0)
        red = (255, 0, 0)
        
        if val < 0:
            return Color(0, 255, 0)
        elif val > 100:
            return Color(255, 0, 0)
        else:
            r = int((red[0] - green[0]) * val / 100 + green[0])
            g = int((red[1] - green[1]) * (100 - val) / 100 + green[1])
            b = int((red[2] - green[2]) * (100 - val) / 100 + green[2])
            return Color(int(r), int(g), int(b))

    @staticmethod
    def getColorForTemperature(val) -> Color:
        green = (0, 255, 0)
        red = (255, 0, 0)
        if val < 0:
            return Color(0, 255, 0)
        elif val > 100:
            return Color(255, 0, 0)
        else:
            r = int((red[0] - green[0]) * val / 100 + green[0])
            g = int((red[1] - green[1]) * (100 - val) / 100 + green[1])
            b = int((red[2] - green[2]) * (100 - val) / 100 + green[2])
            return Color(int(r), int(g), int(b))

    @staticmethod
    def updateLeds():
        print("Updating leds --------------------         ")
        BackgroundLedStrip.CPU_USAGE = SystemUtils.getCpuUsage()
        BackgroundLedStrip.CPU_TEMP = SystemUtils.getCpuTemp()
        BackgroundLedStrip.RAM_USAGE = SystemUtils.getMemoryUsage()

        print(f"CPU Usage: {BackgroundLedStrip.CPU_USAGE}%")
        print(f"CPU Temp: {BackgroundLedStrip.CPU_TEMP}°C")
        print(f"RAM Usage: {BackgroundLedStrip.RAM_USAGE}%")

        maps = Variables.STATUS_LEDS_SETTINGS
        cpuTemp = maps["cpuTemp"]
        cpuUsage = maps["cpuUsage"]
        ramUsage = maps["ramUsage"]

        cpuTempColor = BackgroundLedStrip.getColorFromValue(cpuTemp, BackgroundLedStrip.CPU_TEMP)
        cpuUsageColor = BackgroundLedStrip.getColorFromValue(cpuUsage, BackgroundLedStrip.CPU_USAGE)
        memColor = BackgroundLedStrip.getColorFromValue(ramUsage, BackgroundLedStrip.RAM_USAGE)

        Variables.LED_STRIP[Variables.LED_STRIP.numPixels() - 3] = BackgroundLedStrip.scaleDown(memColor, 1)
        Variables.LED_STRIP[Variables.LED_STRIP.numPixels() - 2] = BackgroundLedStrip.scaleDown(cpuUsageColor, 1)
        Variables.LED_STRIP[Variables.LED_STRIP.numPixels() - 1] = BackgroundLedStrip.scaleDown(cpuTempColor, 1)

        Variables.LED_STRIP.show()

    @staticmethod
    def getColorFromValue(map, val) -> Color:
        for color in map["colors"]:
            if val >= color["start"] and val <= color["end"]:
                return Color(color["color"][0], color["color"][1], color["color"][2])
        return Color(0, 0, 0)

    @staticmethod
    def fill(start, end, r, g, b, brightness):
        for i in range(start, end):
            BackgroundLedStrip.setColor(i, BackgroundLedStrip.getColorWithAlpha(Color(r, g, b), brightness))

    @staticmethod
    def toStringColor(color: Color) -> str:
        return f"({color.r}, {color.g}, {color.b})"
    
    @staticmethod
    def show():
        if(AutomatedDisplayShutdown.isOn()):
            for i in range(BackgroundLedStrip.numPixels()):
                Variables.LED_STRIP[i] = Color(0, 0, 0)
            Variables.LED_STRIP.show()
        else:
            for i in range(BackgroundLedStrip.numPixels()):
                Variables.LED_STRIP[i] = int(BackgroundLedStrip.tmpLeds[i])
            Variables.LED_STRIP.show()

    @staticmethod
    def scaleDown(color: Color, m) -> Color:
        return Color(int(color.r*m), int(color.g*m), int(color.b*m))

    @staticmethod
    def clear():
        BackgroundLedStrip.clearStrip()

    @staticmethod
    def clearStrip():
        BackgroundLedStrip.tmpLeds = [Color(0, 0, 0) for _ in range(BackgroundLedStrip.numPixels())]
        return BackgroundLedStrip.tmpLeds

    @staticmethod
    def setColor(pixel: int, color: Color):
        BackgroundLedStrip.tmpLeds[pixel] = color

    @staticmethod
    def setRGBColor(pixel: int, r: int, g: int, b: int):
        BackgroundLedStrip.setColor(pixel, Color(r, g, b))

    @staticmethod
    def setPixelColorTuple(pixel: int, color: tuple):
        BackgroundLedStrip.setColor(pixel, Color(color[0], color[1], color[2]))

    @staticmethod
    def numPixels():
        return BackgroundLedStrip.LED_COUNT
    
    RAM_USAGE = 0
    CPU_TEMP = 0
    CPU_USAGE = 0

    LED_COUNT = 75
    LED_COUNT_WITH_STATUS_LEDS = 78

    tmpLeds = [Color(0, 0, 0) for _ in range(LED_COUNT)]

