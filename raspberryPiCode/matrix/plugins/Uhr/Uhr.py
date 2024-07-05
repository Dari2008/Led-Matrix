from pytz import timezone
from datetime import datetime
import time as times
from matrix import Variables
from fonts.FontLoader import FontLoader
from leds.BackgroundLedStrip import BackgroundLedStrip
from matrix.Plugin import Plugin


class Uhr:

    def __init__(self, plugin: Plugin) -> None:
        self.plugin = plugin
        self.ISRUNNING = True
        self.plugin.START = self.start
        self.plugin.STOP = self.stop


    def start(self):
        brightness = int(self.plugin.getSetting("brightness", 100))
        bgBrightness = int(self.plugin.getSetting("bgBrightness", 100))
        timeZone = self.plugin.getSetting("timeZone", "Europe/Berlin")
        timeFormat = self.plugin.getSetting("timeFormat", "%H:%M:%S")
        color = self.plugin.getSetting("color", "255,255,255")
        backgroundColor = self.plugin.getSetting("backgroundColor", "0,0,0")
        backgroundDigit = self.plugin.getSetting("backgroundDigit", "SECONDS")
        fontSize = int(self.plugin.getSetting("fontSize", 17))

        print("Uhr started")
        print("Timezone: " + timeZone)
        print("Time Format: " + timeFormat)
        print("Color: " + color)
        print("Background Color: " + backgroundColor)
        print("Background Digit: " + backgroundDigit)
        print("Font Size: " + str(fontSize))
        print("Brightness: " + str(brightness))
        print("Background Brightness: " + str(bgBrightness))

        font = FontLoader.loadFont("Silkscreen", fontSize)

        while self.ISRUNNING:
            time = timezone(timeZone)
            self.drawTime(time, timeFormat, brightness, font, bgBrightness, color, backgroundColor, backgroundDigit)
            times.sleep(0.5)

    def drawTime(self, time, format: str, brightness: int, font, bgBrightness: int, color: str, backgroundColor: str, backgroundDigit: str):
        matrix = Variables.MATRIX

        matrix.clear()
        BackgroundLedStrip.clear()

        currentTime = datetime.now(time)

        timeStr = currentTime.strftime(format)

        colorParsed = color.split(",")
        backgroundColorParsed = backgroundColor.split(",")
        matrix.drawTextInLineCenterWithFont(0, 1, font, timeStr, int(colorParsed[0]), int(colorParsed[1]), int(colorParsed[2]), int(255 * (brightness / 100)), autoOfset=True)

        timeDigit = 0

        if backgroundDigit == "HOURS":
            timeDigit = currentTime.hour
        elif backgroundDigit == "MINUTES":
            timeDigit = currentTime.minute
        elif backgroundDigit == "SECONDS":
            timeDigit = currentTime.second

        if(backgroundDigit == "HOURS"):
            timeDigit = int((Variables.LED_STRIP_LED_COUNT)*(timeDigit / 24))
        else:
            timeDigit = int((Variables.LED_STRIP_LED_COUNT)*(timeDigit / 60))
        
        BackgroundLedStrip.fill(0, timeDigit, int(backgroundColorParsed[0]), int(backgroundColorParsed[1]), int(backgroundColorParsed[2]), int(255 * (bgBrightness / 100)))

        matrix.show()
        BackgroundLedStrip.show()


    def stop(self):
        self.ISRUNNING = False