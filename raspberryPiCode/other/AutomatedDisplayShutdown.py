from datetime import datetime

class AutomatedDisplayShutdown:

    @staticmethod
    def isOn():
        AutomatedDisplayShutdown.checkTime()
        return AutomatedDisplayShutdown.IS_ON
    
    @staticmethod
    def isOff():
        AutomatedDisplayShutdown.checkTime()
        return not AutomatedDisplayShutdown.IS_ON
    
    @staticmethod
    def checkTime():
        currentTime = datetime.now().time()
        currentHour = currentTime.hour

        if currentHour >= 22 or currentHour < 8:
            AutomatedDisplayShutdown.IS_ON = True
        else:
            AutomatedDisplayShutdown.IS_ON = False

    IS_ON = False