from leds.StatusUpdater import StatusUpdater
from leds.BackgroundLedStrip import BackgroundLedStrip
import matrix.Variables as Variables

def run():
    StatusUpdater.run()

def cleanup():
    StatusUpdater.cleanup()