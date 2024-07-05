import threading
from .objs.Food import Food
from .objs.Snake import Snake
from . import Vars
import time
import os
from matrix import Variables
from leds.BackgroundLedStrip import BackgroundLedStrip
from matrix.MatrixClass import MatrixClass
import math
from fonts.FontLoader import FontLoader

class Main(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Variables.MATRIX.setDefaultMethodFont(self.getFontForSize)
        self.running = True
        self.score = 0
        self.deltaTime = 0
        self.showState = "paused"
        self.lastGameFrame = None
        self.food = Food()
        self.snake = Snake(Vars.BODY_PART_COUNT_START, int(Vars.GAME_HEIGHT/2), self.gameEnd, self.setScore, self.getScore)
        Variables.onKeyPress("esc", self.pause)
        Variables.onKeyPress("space", self.resume)
        self.lastTime = time.time()
        self.realLastTime = time.time()
        self.highScore = self.loadHighScore()
        self.oldHighScore = self.highScore

    def getFontForSize(self, size):
        if(size == None):
            return FontLoader.loadFont("Jura", 12)
        return FontLoader.loadFont("Jura", size)

    def reset(self):
        self.snake = Snake(Vars.BODY_PART_COUNT_START, int(Vars.GAME_HEIGHT/2), self.gameEnd, self.setScore, self.getScore)
        self.food = Food()
        self.score = 0

    def gameEnd(self, type):
        self.pause()
        if(self.score > self.highScore):
            self.oldHighScore = self.highScore
            self.highScore = self.score
            self.saveHighScore()
            self.showState = "newhighscore"
        elif(self.score == self.highScore):
            self.showState = "nearhighscore"
        else:
            self.showState = type

    def loadHighScore(self):
        return Vars.PLUGIN.get("highscore", 0)
        
    def saveHighScore(self):
        Vars.PLUGIN.set("highscore", self.highScore)

    def togglePause(self):
        if(self.isPaused()):
            self.resume()
        else:
            self.pause()

    def run(self):
        while self.running:
            self.realLastTime = time.time()

            if(self.showState == "paused"):
                self.showPaused()
            elif(self.showState == "countdown3"):
                self.showCountdown(3)
            elif(self.showState == "countdown2"):
                self.showCountdown(2)
            elif(self.showState == "countdown1"):
                self.showCountdown(1)
            elif(self.showState == "countdown0"):
                self.showCountdown(0)
            elif(self.showState == "game"):
                self.renderGame()
            elif(self.showState == "hitwall"):
                self.showHitWall()
            elif(self.showState == "hitself"):
                self.showHitSelf()
            elif(self.showState == "won"):
                self.showWon()
            elif(self.showState == "newhighscore"):
                self.showNewHighScore()
            elif(self.showState == "nearhighscore"):
                self.showNearHighScore()

            self.deltaTime = time.time() - self.realLastTime

    def showHitWall(self):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 10)
        colorForScore = self.getColorForScore()
        Variables.MATRIX.drawTextInLineCenter(0, 3, "You Hit a Wall", 255, 0, 0, 255)
        Variables.MATRIX.drawTextInLineCenter(1, 3, "Score: " + str(self.score), colorForScore[0], colorForScore[1], colorForScore[2], 255)
        Variables.MATRIX.drawTextInLineCenter(2, 3, "Space To Restart!", 0, 150, 0, 255)
        Variables.MATRIX.show()
        time.sleep(2)

    def showHitSelf(self):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 10)
        colorForScore = self.getColorForScore()
        Variables.MATRIX.drawTextInLineCenter(0, 3, "You Hit Yourself", 255, 0, 0, 255)
        Variables.MATRIX.drawTextInLineCenter(1, 3, "Score: " + str(self.score), colorForScore[0], colorForScore[1], colorForScore[2], 255)
        Variables.MATRIX.drawTextInLineCenter(2, 3, "Space To Restart!", 0, 150, 0, 255)
        Variables.MATRIX.show()
        time.sleep(2)

    def showWon(self):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 10)
        colorForScore = self.getColorForScore()
        Variables.MATRIX.drawTextInLineCenter(0, 3, "You won!", 0, 255, 0, 255)
        Variables.MATRIX.drawTextInLineCenter(1, 3, "Score: " + str(self.score), colorForScore[0], colorForScore[1], colorForScore[2], 255)
        Variables.MATRIX.drawTextInLineCenter(2, 3, "Space To Restart!", 0, 150, 0, 255)
        Variables.MATRIX.show()
        time.sleep(2)

    def showNewHighScore(self):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
            self.wheelOffset = 90
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 10)
        colorForScore = self.getColorForScore()
        self.wheelOffset -= 5
        if(self.wheelOffset < 0):
            self.wheelOffset = 360 + self.wheelOffset
        Variables.MATRIX.drawTextInLineCenter(0, 3, "New Highscore!", type="rgb", wheelOffset=self.wheelOffset)
        Variables.MATRIX.drawTextInLineCenter(1, 3, "Score: " + str(self.score) + "   Old: " + str(self.oldHighScore), colorForScore[0], colorForScore[1], colorForScore[2], 255)
        Variables.MATRIX.drawTextInLineCenter(2, 3, "Space To Restart!", 0, 150, 0, 255)
        Variables.MATRIX.show()

        BackgroundLedStrip.clear()
        degPerLed = 360 / Variables.LED_STRIP_LED_COUNT
        for i in range(Variables.LED_STRIP_LED_COUNT):
            BackgroundLedStrip.setPixelColorTuple(int(i), self.fixBug(MatrixClass.wheel((int(i*degPerLed) % 360) & 255)))
        BackgroundLedStrip.show()
        
        time.sleep(0.01)

    def fixBug(self, color):
        r = color[0]
        g = color[1]
        b = color[2]
        if(r != 0):
            r -= 1
        if(g != 0):
            g -= 1
        if(b != 0):
            b -= 1
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        return (r, g, b)

    def showNearHighScore(self):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 10)
        colorForScore = self.getColorForScore()
        Variables.MATRIX.drawTextInLineCenter(0, 3, "Nearly a Highscore!", 20, 255, 0, 255)
        Variables.MATRIX.drawTextInLineCenter(1, 3, "Score: " + str(self.score) + "   Old: " + str(self.oldHighScore), colorForScore[0], colorForScore[1], colorForScore[2], 255)
        Variables.MATRIX.drawTextInLineCenter(2, 3, "Space To Restart!", 0, 150, 0, 255)
        Variables.MATRIX.show()
        time.sleep(2)

    def getColorForScore(self):
        if(self.score < 10):
            return (255, 0, 0)
        elif(self.score < 20):
            return (255, 120, 0)
        elif(self.score < 30):
            return (255, 255, 0)
        elif(self.score < 40):
            return (0, 255, 0)
        elif(self.score < 50):
            return (0, 255, 255)
        else:
            return (0, 0, 255)


    def showPaused(self):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 50)
        Variables.MATRIX.drawTextCenterCenterWithSize("Paused", 15, 255, 120, 0, 255, True)
        Variables.MATRIX.show()
        time.sleep(0.1)

    def showCountdown(self, number):
        if(self.lastGameFrame == None):
            self.lastGameFrame = Variables.MATRIX.getLastImage()
        Variables.MATRIX.setImage(self.lastGameFrame.copy(), 50)
        if(number == 0):
            Variables.MATRIX.drawTextCenterCenterWithSize("Go!", 20, 0, 255, 0, 255, True)
        else:
            r,g,b = (0, 0, 0)
            if(number == 3):
                r,g,b = (255, 0, 0)
            elif(number == 2):
                r,g,b = (255, 120, 0)
            elif(number == 1):
                r,g,b = (255, 255, 0)

            Variables.MATRIX.drawTextCenterCenterWithSize(str(number), 25, r, g, b, 200, True)
        Variables.MATRIX.show()
        time.sleep(1)

        if(number == 0):
            self.showState = "game"
            self.lastGameFrame = None
        else:
            self.showState = "countdown" + str(number - 1)

    def renderGame(self):
        self.lastTime = time.time()
        self.update()
        self.draw()
        deltaTime = time.time() - self.lastTime
        if(1/Vars.FPS - deltaTime > 0):
            time.sleep(1/Vars.FPS - deltaTime)


    def draw(self):
        Variables.MATRIX.clear()
        self.food.draw(Variables.MATRIX)
        self.snake.draw(Variables.MATRIX)
        Variables.MATRIX.show()
        pass

    def start(self):
        print("Snake game started")
        threading.Thread.start(self)

    def update(self):
        self.snake.move(self.food, self.deltaTime)

    def updateBackgroundLedStrip(self):
        colors = [MatrixClass.wheel(i) for i in range(0, 360, 60)]
        ledsPerCount = 15
        ledsOnStrip = Variables.LED_STRIP_LED_COUNT
        maxCount = int(ledsOnStrip / ledsPerCount)
        rest = self.score / maxCount
        index = math.floor(rest)
        rest = self.score % maxCount
        BackgroundLedStrip.clear()
        if(index == 0):
            for i in range(rest*ledsPerCount):
                BackgroundLedStrip.setPixelColorTuple(i, colors[index])
        else:
            for i in range(ledsOnStrip):
                BackgroundLedStrip.setPixelColorTuple(i, colors[index-1])

            for i in range(rest*ledsPerCount):
                BackgroundLedStrip.setPixelColorTuple(i, colors[index])

        BackgroundLedStrip.show()



    def pause(self):
        if(self.showState != "game"):
            return
        self.showState = "paused"

    def resume(self):
        if(self.showState == "hitwall" or
            self.showState == "hitself" or
            self.showState == "won" or
            self.showState == "newhighscore" or
            self.showState == "nearhighscore"
        ):
            self.reset()
            self.showState = "countdown3"
            return
        if(self.showState == "paused"):
            self.showState = "countdown3"

    def stop(self):
        self.running = False

    def isPaused(self):
        return self.paused
    
    def setScore(self, score):
        self.score = score
        self.updateBackgroundLedStrip()

    def getScore(self):
        return self.score

    def saveScore(self):
        pass

    def isNewHighScore(self):
        return False
    