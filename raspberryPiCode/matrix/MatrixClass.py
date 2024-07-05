from rgbmatrix import RGBMatrix, RGBMatrixOptions, FrameCanvas
from PIL import Image, ImageFont, ImageDraw
import matrix.Variables as Variables
from other.AutomatedDisplayShutdown import AutomatedDisplayShutdown
import re

class MatrixClass:

    def fill(self, x: int, y: int, w: int, h: int, r: int, g: int, b: int, a: int):
        for xx in range(x, x+w):
            for yy in range(y, y+h):
                if xx < 0 or xx >= Variables.MATRIX_WIDTH or yy < 0 or yy >= Variables.MATRIX_HEIGHT:
                    continue
                self.setColor(xx, yy, int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a)))

    def drawLine(self, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, a: int):
        draw = ImageDraw.Draw(self.img)
        draw.line((x1, y1, x2, y2), fill=(int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a))))

    def drawRect(self, x: int, y: int, w: int, h: int, r: int, g: int, b: int, a: int):
        self.drawLine(x, y, x+w, y, r, g, b, a)
        self.drawLine(x, y, x, y+h, r, g, b, a)
        self.drawLine(x+w, y, x+w, y+h, r, g, b, a)
        self.drawLine(x, y+h, x+w, y+h, r, g, b, a)

    def showMatrix(self, x: int, y: int, matrix: list):
        for xx in range(0, len(matrix)):
            for yy in range(0, len(matrix[xx])):
                self.setColor(x+xx, y+yy, matrix[yy][xx][0], matrix[yy][xx][1], matrix[yy][xx][2], 255)

    def setColor(self, x: int, y: int, r: int, g: int, b: int, a: int = 255):
        if x < 0 or x >= Variables.MATRIX_WIDTH or y < 0 or y >= Variables.MATRIX_HEIGHT:
            return
        if(a != 255): 
            self.img.putpixel((x, y), (int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a))))
        else:
            self.img.putpixel((x, y), (r, g, b))

    def setColorRGB(self, x: int, y: int, rgba: int):
        if x < 0 or x >= Variables.MATRIX_WIDTH or y < 0 or y >= Variables.MATRIX_HEIGHT:
            return
        self.img.putpixel((x, y), (int(self.getColorValue((rgba >> 24) & 0xFF, (rgba >> 24) & 0xFF)), int(self.getColorValue((rgba >> 16) & 0xFF, (rgba >> 24) & 0xFF)), int(self.getColorValue((rgba >> 8) & 0xFF, (rgba >> 24) & 0xFF))))

    def drawTextWithFont(self, x: int, y: int, text: str, font, r: int, g: int, b: int, a: int):
        ImageDraw.Draw(self.img).text(xy=(x, y), text=text, font=font, fill=(int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a))))

    def drawText(self, x: int, y: int, text: str, r: int, g: int, b: int, a: int):
        ImageDraw.Draw(self.img).text(xy=(x, y), text=text, fill=(int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a))))

    def drawTextRGB(self, x: int, y: int, text: str, rgbaorR: int, g: int = None, b: int = None, a: int = None):
        if g == None or b == None:
            self.drawText(x, y, text, (rgbaorR >> 24) & 0xFF, (rgbaorR >> 16) & 0xFF, (rgbaorR >> 8) & 0xFF, (rgbaorR >> 24) & 0xFF)
        elif a == None:
            self.drawText(x, y, text, rgbaorR, g, b, 255)
        else:
            self.drawText(x, y, text, rgbaorR, g, b, a)

    def drawTextWithFontRGB(self, x: int, y: int, text: str, font, rgbaorR: int, g: int = None, b: int = None, a: int = None):
        if g == None or b == None:
            self.drawTextWithFont(x, y, text, font, (rgbaorR >> 24) & 0xFF, (rgbaorR >> 16) & 0xFF, (rgbaorR >> 8) & 0xFF, (rgbaorR >> 24) & 0xFF)
        elif a == None:
            self.drawTextWithFont(x, y, text, font, rgbaorR, g, b, 255)
        else:
            self.drawTextWithFont(x, y, text, font, rgbaorR, g, b, a)

    def drawTextCenter(self, y: int, text: str, r: int, g: int, b: int, a: int):
        self.drawText((Variables.MATRIX_WIDTH - ImageDraw.Draw(self.img).textlength(text)) / 2, y, text, r, g, b, a)

    def drawTextCenterRGB(self, y: int, text: str, rgbaorR: int, g: int = None, b: int = None, a: int = None):
        self.drawTextRGB((Variables.MATRIX_WIDTH - ImageDraw.Draw(self.img).textlength(text)) / 2, y, text, rgbaorR, g, b, a)

    def drawTextCenterWithFont(self, y: int, text: str, font, r: int, g: int, b: int, a: int):
        self.drawTextWithFont((Variables.MATRIX_WIDTH - ImageDraw.Draw(self.img).textlength(text, font=font)) / 2, y, text, font, r, g, b, a)

    def drawTextCenterWithFontRGB(self, y: int, text: str, font, rgbaorR: int, g: int = None, b: int = None, a: int = None):
        self.drawTextWithFontRGB((Variables.MATRIX_WIDTH - ImageDraw.Draw(self.img).textlength(text, font=font)) / 2, y, text, font, rgbaorR, g, b, a)

    def drawTextCenterCenter(self, text: str, r: int, g: int, b: int, a: int):
        self.drawTextInLineCenter(0, 1, text, r, g, b, a)

    def drawTextCenterCenterWithSize(self, text: str, size, r: int, g: int, b: int, a: int, autoOfset = False):
        self.drawTextInLineCenterWithSize(0, 1, text, size, r, g, b, a, autoOfset=autoOfset)

    def drawTextInLineCenterWithFont(self, line: int, totalLines: int, font, text: str, r: int=0, g: int=0, b: int=0, a: int=0, type: str = "onecolor", wheelOffset=90, autoOfset = False):
        draw = ImageDraw.Draw(self.img)
        textsize = draw.textbbox(xy=(0, 0), text=self.filteransiColors(text), font=font)
        width = textsize[2] - textsize[0]
        height = textsize[3] - textsize[1] + (0 if not autoOfset else font.size)

        totHeight = int(Variables.MATRIX_HEIGHT / totalLines)
        if(type == "onecolor"):
            allreadyWidth = 0
            defaultFill = (int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a)))
            currentFill = defaultFill
            i = 0
            while i < len(text):
                char = text[i]
                if(char == "\u001B"):
                    if (text[i+1] == "["):
                        i += 2
                    else:
                        continue
                    firstNum = text[i]
                    i += 1
                    secondNum = text[i]
                    i += 2 # for the m
                    num = int((firstNum + "" +  secondNum))
                    if(num == 0):
                        currentFill = defaultFill
                    else:
                        currentFill = MatrixClass.COLOR_ANSI_CODES[num]
                    continue

                x = (Variables.MATRIX_WIDTH/2 - width/2) + allreadyWidth + (draw.textlength(char, font=font) / 2)
                allreadyWidth += draw.textlength(char, font=font)
                draw.text(
                    xy=(int(x), int(totHeight*line + totHeight/2 - height/2)),
                    text=char,
                    fill=currentFill,
                    font=font
                )
                i += 1
        elif(type == "rgb"):
            stepSize = 360 / len(text)
            i = 0
            allreadyWidth = 0
            for char in text:
                x = (Variables.MATRIX_WIDTH/2 - width/2) + allreadyWidth + (draw.textlength(char, font=font) / 2)
                allreadyWidth += draw.textlength(char, font=font)
                draw.text(
                    xy=(int(x), int(totHeight*line + totHeight/2 - height/2)),
                    text=char,
                    fill=self.wheel((wheelOffset + i*stepSize) % 360),
                    font=font
                )
                i += 1

    def filteransiColors(self, text:str):
        ansi_escape = re.compile(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]')
        return ansi_escape.sub('', text)

    def drawTextInLineCenter(self, line: int, totalLines: int, text: str, r: int=0, g: int=0, b: int=0, a: int=0, type: str = "onecolor", wheelOffset=90):
        self.drawTextInLineCenterWithFont(
            line=line, 
            totalLines=totalLines, 
            font= None if self.defaultFont == None else (self.defaultFont if (isinstance(self.defaultFont, ImageFont.ImageFont) or isinstance(self.defaultFont, ImageFont.FreeTypeFont)) else self.defaultFont(None)),
            text=text, 
            r=r, 
            g=g, 
            b=b, 
            a=a, 
            type=type, 
            wheelOffset=wheelOffset
        )

    def drawTextInLineCenterWithSize(self, line: int, totalLines: int, text: str, size: int = 10, r: int=0, g: int=0, b: int=0, a: int=0, type: str = "onecolor", wheelOffset=90, autoOfset = False):
        if(self.defaultFont == None):
            return
        if(isinstance(self.defaultFont, ImageFont.ImageFont) or isinstance(self.defaultFont, ImageFont.FreeTypeFont)):
            self.drawTextInLineCenterWithFont(
                line=line, 
                totalLines=totalLines, 
                font=self.defaultFont, 
                text=text, 
                r=r, 
                g=g, 
                b=b, 
                a=a, 
                type=type, 
                wheelOffset=wheelOffset,
                autoOfset=autoOfset
            )
        else:
            self.drawTextInLineCenterWithFont(
                line=line, 
                totalLines=totalLines, 
                font=self.defaultFont(size), 
                text=text, 
                r=r, 
                g=g, 
                b=b, 
                a=a, 
                type=type, 
                wheelOffset=wheelOffset,
                autoOfset=autoOfset
            )

    def drawTextFloatRight(self, text: str, x: int, y: int, r: int, g: int, b: int, a: int):
        draw = ImageDraw.Draw(self.img)
        textsize = draw.textbbox(xy=(0, 0), text=text)
        width = textsize[2] - textsize[0]
        draw.text(
            xy=(x - width, y),
            text=text,
            fill=(int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a)))
        )

    def drawTextFloatLeft(self, text: str, x: int, y: int, r: int, g: int, b: int, a: int):
        draw = ImageDraw.Draw(self.img)
        draw.text(
            xy=(x, y),
            text=text,
            fill=(int(self.getColorValue(r, a)), int(self.getColorValue(g, a)), int(self.getColorValue(b, a)))
        )

    @staticmethod
    def wheel(pos):
        if pos < 85:
            return (int(pos * 3), int(255 - pos * 3), 0)
        elif pos < 170:
            pos -= 85
            return (int(255 - pos * 3), 0, int(pos * 3))
        else:
            pos -= 170
            return (0, int(pos * 3), int(255 - pos * 3))

    def show(self, keepImage: bool = False):
        if(AutomatedDisplayShutdown.isOn()):
            self.MATRIX.SetImage(Image.new(mode="RGB", size=(Variables.MATRIX_WIDTH, Variables.MATRIX_HEIGHT)))
        else:
            self.MATRIX.SetImage(self.img)
            self.lastimage = self.img
            if(not keepImage):
                self.createNewImage()

    def getLastImage(self) -> Image:
        return self.lastimage

    def getColorValue(self, value, alpha) -> int:
        return int(value * self.map(alpha, 0, 255, 0, 1))

    def createNewImage(self):
        self.img = Image.new(mode="RGB", size=(Variables.MATRIX_WIDTH, Variables.MATRIX_HEIGHT))

    def map(self, x, in_min, in_max, out_min, out_max) -> float:
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def getCurrentImage(self) -> Image:
        return self.img

    def setImage(self, img: Image, opacity: int = 100):
        if(opacity == 100):
            self.img = img
            return
        self.img = Image.blend(self.img, img, opacity/100)

    def clear(self):
        self.img = Image.new(mode="RGB", size=(Variables.MATRIX_WIDTH, Variables.MATRIX_HEIGHT))

    def drawImage(self, imgs: Image, x: int, y: int):
        self.img.paste(imgs, (x, y))

    def setBrightness(self, brightness: int):
        self.MATRIX.brightness = brightness
        if(self.lastimage == None):
            return
        currentImage = self.getCurrentImage()
        self.setImage(self.lastimage)
        self.show()
        self.setImage(currentImage)

    def setDefaultFont(self, font):
        self.defaultFont = font

    def getDefaultFont(self):
        return self.defaultFont
    
    def setDefaultMethodFont(self, method):
        self.defaultFont = method

    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = Variables.MATRIX_PANEL_WIDTH
        options.cols = Variables.MATRIX_PANEL_HEIGHT
        options.gpio_slowdown = Variables.GPIO_SLOWDOWN
        options.chain_length = Variables.CHAIN_LENGTH
        options.parallel = Variables.PARALLEL
        options.pwm_lsb_nanoseconds = 70
        self.MATRIX = RGBMatrix(options=options)
        self.createNewImage()
        self.defaultFont = None
        pass

    COLOR_ANSI_CODES = {
        30: "black",
        31: "red",
        32: "green",
        33: "yellow",
        34: "blue",
        35: "magenta",
        36: "cyan",
        37: "white",
        39: "default",
        90: "gray",
        91: "brightRed",
        92: "brightGreen",
        93: "brightYellow",
        94: "brightBlue",
        95: "brightMagenta",
        96: "brightCyan",
        97: "brightWhite"
    }