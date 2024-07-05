import time
from pyudev import Context
import keyboard
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
from multiprocessing import shared_memory
from KeyboardMap import KeyboardMap
import atexit
import argparse
import threading

shm = None

def isKeyboardConnected():
    context = Context()
    for device in context.list_devices(subsystem='input'):
        if 'ID_INPUT_KEYBOARD' in device.properties:
            return True
    return False

def getSharedMemory():
    return shared_memory.SharedMemory(name="matrix")

def onPress(key):
    global args
    global shm
    if not args.debug:
        shm.buf[KeyboardMap.getKey(key)] = 1
    else:
        print(key, KeyboardMap.getKey(key), "pressed")

def onRelease(key):
    global args
    global shm
    if not args.debug:
        shm.buf[KeyboardMap.getKey(key)] = 0
    else:
        print(key, KeyboardMap.getKey(key), "released")

def onAction(event):
    if event.event_type == KEY_DOWN:
        onPress(event.name)

    elif event.event_type == KEY_UP:
        onRelease(event.name)

def keyboardListener():
    if(args.debug):
        print("Waiting for keyboard connection")
    while not isKeyboardConnected():
        time.sleep(0.5)
        if(args.debug):
            print("Keyboard not connected")

    if(args.debug):
        print("Keyboard connected")
    try:
        keyboard.hook(lambda e: onAction(e))
    except Exception as e:
        keyboardListener()
        return

    if(args.debug):
        print("Keyboard listener started")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        if not args.debug:
            shm.close()
        exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyboard input")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    if args.debug:
        print("Debug mode")
    else:
        shm = getSharedMemory()
        atexit.register(shm.close)

    keyboard_thread = threading.Thread(target=keyboardListener)
    keyboard_thread.start()

    try:
        while True:
            # Hier können Sie den restlichen Code des Hauptprogramms einfügen
            time.sleep(1)  # Beispiel: Das Hauptprogramm wartet 1 Sekunde
    except KeyboardInterrupt:
        if not args.debug:
            shm.close()
        exit(0)
