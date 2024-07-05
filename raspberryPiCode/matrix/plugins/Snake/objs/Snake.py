from ..objs.SnakePart import SnakePart
from ..objs.Food import Food
from ..other.Collision import Collision
from .. import Vars
from matrix import Variables

class Snake:
    def __init__(self, spawnX, spawnY, gameEnd, setScore, getScore) -> None:
        self.dir = "right"
        self.head = SnakePart(spawnX, spawnY)
        self.tale = []
        self.setScore = setScore
        self.getScore = getScore
        self.gameEnd = gameEnd
        self.timePassedSinceUpdate = 0
        self.lastDir = "right"
        self.removeLast = True

        self.initTale()
        self.initKeys()

    def initTale(self):
        for i in range(1, Vars.BODY_PART_COUNT_START):
            coors = self.head.getPos() 
            self.tale.append(SnakePart(coors[0] - i, coors[1]))

    def initKeys(self):
        Variables.onKeyPress("w", lambda: self.changeDir("up"))
        Variables.onKeyPress("a", lambda: self.changeDir("left"))
        Variables.onKeyPress("s", lambda: self.changeDir("down"))
        Variables.onKeyPress("d", lambda: self.changeDir("right"))
        Variables.onKeyPress("d", lambda: self.changeDir("right"))
        Variables.onKeyPress("up", lambda: self.changeDir("up"))
        Variables.onKeyPress("left", lambda: self.changeDir("left"))
        Variables.onKeyPress("down", lambda: self.changeDir("down"))
        Variables.onKeyPress("right", lambda: self.changeDir("right"))
        print("Keys initialized")


    def draw(self, matrix):

        for i in range(0, len(self.tale)):
            part = self.tale[i]
            nextPart = None if i == len(self.tale) - 1 else self.tale[i + 1]
            prevPart = self.head if i == 0 else self.tale[i - 1]
            part.draw(matrix, False, nextPart, prevPart)

        self.head.draw(matrix, True, None, None, self.dir, self.lastDir)


    def move(self, food, deltaTime):

        self.timePassedSinceUpdate += deltaTime
        if(self.timePassedSinceUpdate < Vars.SNAKE_SPEED_TIME):
            return

        self.timePassedSinceUpdate = 0

        x, y = self.head.getPos()
        if self.dir == "up":
            y -= 1
        elif self.dir == "down":
            y += 1
        elif self.dir == "left":
            x -= 1
        elif self.dir == "right":
            x += 1

        print("Moving", x, ":", y)

        collision = self.checkCollision(food)

        if(not collision):
            self.moveTale(x, y)
            self.lastDir = self.dir
        else:
            self.gameEnd(collision)

    def moveTale(self, x, y):
        newPart = SnakePart(x, y)
        self.tale.insert(0, self.head)
        self.head = newPart
        if self.removeLast:
            del self.tale[-1]
        else:
            self.removeLast = True

    def checkCollision(self, food) -> bool | str | None:
        if(Collision.didCollideWithFood(self, food)):
            self.eat(food)
            return
        
        if(Collision.didHitWall(self)):
            return "hitwall"
        
        if(Collision.didHitSelf(self)):
            return "hitself"
    
        return False
        
    def eat(self, food: Food):
        self.setScore(self.getScore() + 1)
        self.removeLast = False
        food.respawn(self)
        print("Eating")

    def changeDir(self, dir):
        if(dir == "left"):
            if(self.lastDir != "right"):
                self.dir = "left"
        elif(dir == "right"):
            if(self.lastDir != "left"):
                self.dir = "right"
        elif(dir == "up"):
            if(self.lastDir != "down"):
                self.dir = "up"
        elif(dir == "down"):
            if(self.lastDir != "up"):
                self.dir = "down"

    def getPos(self):
        return self.head.getPos()
    
    def getDir(self):
        return self.dir
    
    def getTale(self):
        return self.tale
    
    def getHead(self):
        return self.head
    
