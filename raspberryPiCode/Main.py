from matrix import Main as ServerMain
from leds import Main as LedMain
from matrix import Variables
from buttons import Main as ButtonMain


def startAll():
    print("Started")
    Variables.startKeyboardListener()
    ServerMain.init()
    LedMain.run()
    ButtonMain.run()
    ServerMain.run()
    print("Stopping...")
    ServerMain.clear()
    LedMain.cleanup()
    Variables.cleanup()
    print("Stopped")

if __name__ == "__main__":
    startAll()