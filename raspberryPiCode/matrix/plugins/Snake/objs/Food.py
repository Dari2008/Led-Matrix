import matrix.Variables as Variables
from ..other.Collision import Collision
import random
from .. import Vars

class Food:
    
    def __init__(self):
        self.x = random.randint(0, int(Variables.MATRIX_WIDTH / Vars.TILE_SIZE)-1)
        self.y = random.randint(0, int(Variables.MATRIX_HEIGHT / Vars.TILE_SIZE)-1)
        self.screenX = self.x * Vars.TILE_SIZE
        self.screenY = self.y * Vars.TILE_SIZE

        self.coordinates = (self.x, self.y)
        self.screenCoordinates = (self.screenX, self.screenY)

    def draw(self, matrix):
        matrix.showMatrix(self.screenX, self.screenY, Vars.FOOD_DATA)

    def respawn(self, snake):

        while(Collision.didCollideWithFoodFromCoords(snake.getPos(), (self.x, self.y))):
            self.x = random.randint(0, int(Variables.MATRIX_WIDTH / Vars.TILE_SIZE)-1)
            self.y = random.randint(0, int(Variables.MATRIX_HEIGHT / Vars.TILE_SIZE)-1)
            print("New Food At: ", self.x, ":", self.y)

        self.screenX = self.x * Vars.TILE_SIZE
        self.screenY = self.y * Vars.TILE_SIZE

        self.coordinates = (self.x, self.y)
        self.screenCoordinates = (self.screenX, self.screenY)

    def getPos(self):
        return self.coordinates
    
    def getScreenPos(self):
        return self.screenCoordinates
    
    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.screenX = x * Vars.TILE_SIZE
        self.screenY = y * Vars.TILE_SIZE
        self.coordinates = (self.x, self.y)
        self.screenCoordinates = (self.screenX, self.screenY)

    def setScreenPos(self, x, y):
        self.screenX = x
        self.screenY = y
        self.x = int(x / Vars.TILE_SIZE)
        self.y = int(y / Vars.TILE_SIZE)
        self.coordinates = (self.x, self.y)
        self.screenCoordinates = (self.screenX, self.screenY)