from .. import Vars
from matrix import Variables
from .. import Vars

class Collision:

    @staticmethod
    def didCollideWithFoodFromCoords(coords1, coords2):
        if coords1 == coords2:
            return True
        return False

    @staticmethod
    def didCollideWithFood(snake, food):
        return Collision.didCollideWithFoodFromCoords(snake.getPos(), food.getPos())
    
    @staticmethod
    def didHitWall(snake):
        x, y = snake.getPos()
        GAME_WIDTH = Vars.GAME_WIDTH
        GAME_HEIGHT = Vars.GAME_HEIGHT

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        
        return False
    
    @staticmethod
    def didHitSelf(snake):
        x, y = snake.getPos()
        tale = snake.getTale()
        for i in range(0, len(tale)):
            taleX, taleY = tale[i].getPos()
            if x == taleX and y == taleY:
                return True
        return False