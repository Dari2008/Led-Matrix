from .. import Vars

class SnakePart:
    def __init__(self, x, y, isScreen = False) -> None:
        if(isScreen):
            self.screenX = x
            self.screenY = y
            self.x = int(x / Vars.TILE_SIZE)
            self.y = int(y / Vars.TILE_SIZE)
        else:
            self.x = x
            self.y = y
            self.screenX = x * Vars.TILE_SIZE
            self.screenY = y * Vars.TILE_SIZE

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.screenX = x * Vars.TILE_SIZE
        self.screenY = y * Vars.TILE_SIZE

    def draw(self, matrix, isHead = False, nextPart=None, prevPart=None, currentDir = "up", lastDir = "up"):
        if(isHead):
            if lastDir == currentDir:
                matrix.showMatrix(
                    self.screenX, 
                    self.screenY, 
                    Vars.SNAKE_HEAD_DATA[currentDir]
                )
            else:
                matrix.showMatrix(
                    self.screenX, 
                    self.screenY, 
                    Vars.CURVE_HEAD_CURVE_DATA[lastDir + "_" + currentDir]
                )

        else:
            nextPartDirection = None
            prevPartDirection = None

            if(nextPart != None):
                nextPartDirection = (nextPart.x - self.x, nextPart.y - self.y)
                match(nextPartDirection):
                    case (0, 1):
                        nextPartDirection = "down"
                    case (0, -1):
                        nextPartDirection = "up"
                    case (1, 0):
                        nextPartDirection = "right"
                    case (-1, 0):
                        nextPartDirection = "left"
                    case _:
                        print(nextPartDirection)

            if(prevPart != None):
                prevPartDirection = (prevPart.x - self.x, prevPart.y - self.y)
                match(prevPartDirection):
                    case (0, 1):
                        prevPartDirection = "down"
                    case (0, -1):
                        prevPartDirection = "up"
                    case (1, 0):
                        prevPartDirection = "right"
                    case (-1, 0):
                        prevPartDirection = "left"
                    case _:
                        print(prevPartDirection)

            if(nextPartDirection == None):
                if(prevPartDirection == "up"):
                    nextPartDirection = "down"
                elif(prevPartDirection == "down"):
                    nextPartDirection = "up"
                elif(prevPartDirection == "left"):
                    nextPartDirection = "right"
                elif(prevPartDirection == "right"):
                    nextPartDirection = "left"
                else:
                    nextPartDirection = "up"

            if(nextPartDirection == "up" and prevPartDirection == "down" or nextPartDirection == "down" and prevPartDirection == "up"):
                matrix.fill(
                    self.screenX + int((Vars.TILE_SIZE - Vars.SNAKE_TALE_WIDTH) / 2), 
                    self.screenY, 
                    Vars.SNAKE_TALE_WIDTH, 
                    Vars.TILE_SIZE, 
                    Vars.SNAKE_COLOR[0], 
                    Vars.SNAKE_COLOR[1], 
                    Vars.SNAKE_COLOR[2], 
                    255
                )
            elif(nextPartDirection == "left" and prevPartDirection == "right" or nextPartDirection == "right" and prevPartDirection == "left"):
                matrix.fill(
                    self.screenX, 
                    self.screenY + int((Vars.TILE_SIZE - Vars.SNAKE_TALE_WIDTH) / 2), 
                    Vars.TILE_SIZE, 
                    Vars.SNAKE_TALE_WIDTH, 
                    Vars.SNAKE_COLOR[0], 
                    Vars.SNAKE_COLOR[1], 
                    Vars.SNAKE_COLOR[2], 
                    255
                )

            else:
                first = None
                second = None

                if(nextPartDirection == "up" or nextPartDirection == "down"):
                    first = prevPartDirection
                    second = nextPartDirection
                else:
                    first = nextPartDirection
                    second = prevPartDirection

                if(isinstance(first, tuple) or isinstance(second, tuple)):
                    return

                matrix.showMatrix(
                    self.screenX,
                    self.screenY,
                    Vars.CURVE_TALE_PART_DATA[first + "_" + second]
                )


    def setScreenPos(self, x, y):
        self.screenX = x
        self.screenY = y
        self.x = int(x / Vars.TILE_SIZE)
        self.y = int(y / Vars.TILE_SIZE)

    def getPos(self):
        return (self.x, self.y)
    
    def getScreenPos(self):
        return (self.screenX, self.screenY)

    def getIndex(self):
        return self.index