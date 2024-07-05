from leds.BackgroundLedStrip import BackgroundLedStrip
import threading
import time

class StatusUpdater:

    @staticmethod
    def run():
        StatusUpdater.THREAD = threading.Thread(target=StatusUpdater.startLoop, daemon=True)
        StatusUpdater.THREAD.start()
        StatusUpdater.SLEEP_TIMINGS = 1
        StatusUpdater.SLEEP_TIME = 60

    @staticmethod
    def cleanup():
        StatusUpdater.RUNNING = False

    @staticmethod
    def startLoop():
        while StatusUpdater.RUNNING:
            BackgroundLedStrip.updateLeds()
            for i in range(0, int(StatusUpdater.SLEEP_TIME/StatusUpdater.SLEEP_TIMINGS)-1):
                if(StatusUpdater.RUNNING == False):
                    return
                time.sleep(StatusUpdater.SLEEP_TIMINGS)

            if(StatusUpdater.SLEEP_TIME%StatusUpdater.SLEEP_TIMINGS != 0):
                if(StatusUpdater.RUNNING == False):
                    return
                time.sleep(StatusUpdater.SLEEP_TIME%StatusUpdater.SLEEP_TIMINGS)
            
            pass

    THREAD = None
    RUNNING = True
    SLEEP_TIMINGS = 1
    SLEEP_TIME = 10