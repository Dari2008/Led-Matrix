from . import Vars as Vars
from matrix import Variables as Variables

class Paddle:

    def __init__(self, x, keyUp = "w", keyDown = "s"):
        self.x = x
        self.keyUp = keyUp
        self.keyDown = keyDown

    def move(self, key):
        if key == self.keyUp:
            self.x -= Vars.PADDLE_MOVE_SPEED * Vars.DELTA_TIME
        elif key == self.keyDown:
            self.x += Vars.PADDLE_MOVE_SPEED * Vars.DELTA_TIME

        if self.x < 0:
            self.x = 0
        elif self.x > Variables.MATRIX_WIDTH - Vars.PADDLE_WIDTH:
            self.x = Variables.MATRIX_WIDTH - Vars.PADDLE_WIDTH

    def draw(self, matrix):
        for y in range(Variables.MATRIX_HEIGHT):
            for x in range(Vars.PADDLE_WIDTH):
                matrix.setPixel(self.x + x, y, 1)

    def getRect(self):
        return self.x, 0, Vars.PADDLE_WIDTH, Variables.MATRIX_HEIGHT
    
    def getCenter(self):
        return self.x + Vars.PADDLE_WIDTH // 2, Variables.MATRIX_HEIGHT // 2
    
    