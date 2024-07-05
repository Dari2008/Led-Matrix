import os
import sys
from matrix.MatrixClass import MatrixClass
from matrix import Server as Server
from leds.BackgroundLedStrip import BackgroundLedStrip
from rpi_ws281x import PixelStrip, Color, ws
import threading
import time
from multiprocessing import shared_memory
from keyboardListener.KeyboardMap import KeyboardMap
import json
from buttons.Actions import Actions

shm = shared_memory.SharedMemory(name="matrix", create=True, size=1000)

keyListeners = []
listener = None
oldStates = [0 for i in range(1000)]

def keyListenerLoop():
    while True:
        for keyListener in keyListeners:
            if(keyListener["type"] == "press"):
                if(isKeyPressed(keyListener["key"]) and oldStates[keyListener["key"]] == 0):
                    keyListener["callback"]()
            elif(keyListener["type"] == "release"):
                if(not isKeyPressed(keyListener["key"]) and oldStates[keyListener["key"]] == 1):
                    keyListener["callback"]()
            elif(keyListener["type"] == "both"):
                if(isKeyPressed(keyListener["key"]) and oldStates[keyListener["key"]] == 0):
                    keyListener["callback"]()
                elif(not isKeyPressed(keyListener["key"]) and oldStates[keyListener["key"]] == 1):
                    keyListener["callback"]()
        time.sleep(0.1)

def run():
    global keyListeners
    global shm
    threading.Thread(target=keyListenerLoop, daemon=True).start()

def isKeyPressed(key):
    return shm.buf[key] == 1

def setKeyPressed(key):
    shm.buf[key] = 1

def setKeyReleased(key):
    shm.buf[key] = 0

def setKeyReleasedAll():
    for i in range(1000):
        shm.buf[i] = 0

def onKeyPress(key, callback):
    keyListeners.append({
        "key": KeyboardMap.getKey(key),
        "callback": callback,
        "type": "press"
    })

def onKeyRelease(key, callback):
    keyListeners.append({
        "key": KeyboardMap.getKey(key),
        "callback": callback,
        "type": "release"
    })

def onKey(key, callback):
    keyListeners.append({
        "key": KeyboardMap.getKey(key),
        "callback": callback,
        "type": "both"
    })

def removeKeyListener(key):
    for keyListener in keyListeners:
        if(keyListener["key"] == key):
            keyListeners.remove(keyListener)


def cleanup():
    global shm
    global listener
    listener.close()
    shm.close()
    shm.unlink()

def startKeyboardListener():
    global listener
    listener = os.popen("sudo python keyboardListener/Main.py")
    run()


MIN_PORT = 4000
MAX_PORT = 8000
PLUGIN_DIR = "./matrix/plugins/"
IMAGE_DIR = "./images/"
GIF_DIR = "./gifs/"
TMP_DIR = "./tmp/"
CORE_SETTINGS = "./coreSettings/"
SETTINGS_DIR = "./settings/"

LAST_USED_PATH = CORE_SETTINGS + "lastUsed.json"

HOST = "192.168.178.24" # 192.168.178.24
MAIN_PORT = 1234
GPIO_SLOWDOWN = 3
CHAIN_LENGTH = 2
PARALLEL = 1
MATRIX_PANEL_WIDTH = 64
MATRIX_PANEL_HEIGHT = 64
MATRIX_WIDTH = 128
MATRIX_HEIGHT = 64

CHUNK_SIZE = 64

LED_STRIP_FREQ_HZ = 800000
LED_STRIP_DATA_PIN = 21
LED_STRIP_LED_BRIGHTNESS = 255
LED_STRIP_COUNT = 78
LED_STRIP_LED_COUNT = 75

LED_STRIP_TOP = [
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27
]
LED_STRIP_BOTTOM = [
    64,
    63,
    62,
    61,
    60,
    59,
    58,
    57,
    56,
    55,
    54,
    53,
    52,
    51,
    50,
    49,
    48,
    47,
    46,
    45,
    44,
    43,
    42,
    41,
    40
]
LED_STRIP_RIGHT = [
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39
]
LED_STRIP_LEFT = [
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
	0,
	1,
	2
]



BTN_PICTURE_PIN = 21
BTN_ANIMATION_PIN = 20
BTN_PLUGIN_PIN = 16
BTN_NEXT_PIN = 26

STATUS_LEDS_SETTINGS = {
    "cpuTemp":{
        "colors": [
            {
                "start": 0,
                "end": 30,
                "color": (0, 255, 0)
            },
            {
                "start": 30,
                "end": 50,
                "color": (255, 255, 0)
            },
            {
                "start": 50,
                "end": 70,
                "color": (255, int(255/2), 0)
            },
            {
                "start": 70,
                "end": 100,
                "color": (255, 0, 0)
            }
        ]
    },
    "cpuUsage":{
        "colors": [
            {
                "start": 0,
                "end": 30,
                "color": (0, 255, 0)
            },
            {
                "start": 30,
                "end": 50,
                "color": (255, 255, 0)
            },
            {
                "start": 50,
                "end": 70,
                "color": (255, int(255/2), 0)
            },
            {
                "start": 70,
                "end": 100,
                "color": (255, 0, 0)
            }
        ]
    },
    "ramUsage": {
        "colors": [
            {
                "start": 0,
                "end": 30,
                "color": (0, 255, 0)
            },
            {
                "start": 30,
                "end": 50,
                "color": (255, 255, 0)
            },
            {
                "start": 50,
                "end": 70,
                "color": (255, int(255/2), 0)
            },
            {
                "start": 70,
                "end": 100,
                "color": (255, 0, 0)
            }
        ]
    }
}

MATRIX: MatrixClass = None
SERVER: Server = None
LED_STRIP = PixelStrip(
    LED_STRIP_COUNT, 
    LED_STRIP_DATA_PIN, 
    LED_STRIP_FREQ_HZ, 
    10, #10
    False, 
    LED_STRIP_LED_BRIGHTNESS, 
    0, 
    strip_type=ws.WS2812_STRIP
)
LED_STRIP.begin()
for i in range(LED_STRIP.numPixels()):
    LED_STRIP.setPixelColor(i, Color(0, 0, 0))
LED_STRIP.show()

ACTIONS: Actions = None

LAST_USED_DATA = {
    "lastImagePath": None,
    "lastGifPath": None,
    "lastPlugin": None
}

def saveLastUsedData():
    global LAST_USED_DATA
    with open(LAST_USED_PATH, "w") as f:
        f.write(json.dumps(LAST_USED_DATA))

def loadLastUsedData():
    global LAST_USED_DATA
    if(not os.path.exists(LAST_USED_PATH)):
        return
    with open(LAST_USED_PATH, "r") as f:
        red = f.read()
        LAST_USED_DATA = json.loads(red)

def createDirs():
    createDir(PLUGIN_DIR)
    createDir(IMAGE_DIR)
    createDir(GIF_DIR)
    createDir(TMP_DIR)
    createDir(SETTINGS_DIR)
    createDir(CORE_SETTINGS)

def createDir(path: str):
    if(not os.path.exists(path)):
        os.mkdir(path)
        print(f"Created {path} directory")

def set_permissions_recursive(directory_path, permissions):
    os.chmod(directory_path, permissions)
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, permissions)
    
    for root, dirs, _ in os.walk(directory_path):
        for directory in dirs:
            subdirectory_path = os.path.join(root, directory)
            set_permissions_recursive(subdirectory_path, permissions)

createDirs()

set_permissions_recursive(PLUGIN_DIR, 0o777)
set_permissions_recursive(IMAGE_DIR, 0o777)
set_permissions_recursive(GIF_DIR, 0o777)
set_permissions_recursive(TMP_DIR, 0o777)
set_permissions_recursive(SETTINGS_DIR, 0o777)
set_permissions_recursive(CORE_SETTINGS, 0o777)

loadLastUsedData()
print(LAST_USED_DATA)