import matrix.Variables as Variables
from . import Images
from matrix.Plugin import Plugin

SNAKE_HEAD_WIDTH = 6
SNAKE_TALE_WIDTH = 4
TILE_SIZE = 6
SPEED = 6
BODY_PART_COUNT_START = 3
SNAKE_HEAD_COLOR = (55, 136, 55)
SNAKE_COLOR = (0, 136, 0)
FOOD_COLOR = (255, 0, 0)
FPS = 60

PLUGIN: Plugin = None

FOOD_DATA = Images.loadImage(Images.FOOD, Images.NUMBER_COLOR_MAP)

CURVE_TALE_PART_DATA = {
    "left_down": Images.loadImage(Images.CURVE_TALE_LEFT_DOWN, Images.NUMBER_COLOR_MAP),
    "left_up": Images.loadImage(Images.CURVE_TALE_LEFT_UP, Images.NUMBER_COLOR_MAP),
    "right_down": Images.loadImage(Images.CURVE_TALE_RIGHT_DOWN, Images.NUMBER_COLOR_MAP),
    "right_up": Images.loadImage(Images.CURVE_TALE_RIGHT_UP,Images. NUMBER_COLOR_MAP)
}
SNAKE_HEAD_DATA = {
    "up": Images.loadImage(Images.SNAKE_HEAD_UP, Images.NUMBER_COLOR_MAP),
    "down": Images.loadImage(Images.SNAKE_HEAD_DOWN, Images.NUMBER_COLOR_MAP),
    "left": Images.loadImage(Images.SNAKE_HEAD_LEFT, Images.NUMBER_COLOR_MAP),
    "right": Images.loadImage(Images.SNAKE_HEAD_RIGHT,Images. NUMBER_COLOR_MAP)
}


CURVE_HEAD_CURVE_DATA = {
    "right_down": Images.loadImage(Images.CURVE_HEAD_CURVE_RIGHT_DOWN, Images.NUMBER_COLOR_MAP),
    "right_up": Images.loadImage(Images.CURVE_HEAD_CURVE_RIGHT_UP, Images.NUMBER_COLOR_MAP),
    "left_down": Images.loadImage(Images.CURVE_HEAD_CURVE_LEFT_DOWN, Images.NUMBER_COLOR_MAP),
    "left_up": Images.loadImage(Images.CURVE_HEAD_CURVE_LEFT_UP, Images.NUMBER_COLOR_MAP),
    "down_left": Images.loadImage(Images.CURVE_HEAD_CURVE_DOWN_LEFT, Images.NUMBER_COLOR_MAP),
    "down_right": Images.loadImage(Images.CURVE_HEAD_CURVE_DOWN_RIGHT, Images.NUMBER_COLOR_MAP),
    "up_left": Images.loadImage(Images.CURVE_HEAD_CURVE_UP_LEFT, Images.NUMBER_COLOR_MAP),
    "up_right": Images.loadImage(Images.CURVE_HEAD_CURVE_UP_RIGHT,Images. NUMBER_COLOR_MAP)
}

SNAKE_SPEED_TIME = 1 / SPEED

score = 0
highscore = 0

GAME_WIDTH = int(Variables.MATRIX_WIDTH / TILE_SIZE)
GAME_HEIGHT = int(Variables.MATRIX_HEIGHT / TILE_SIZE)
