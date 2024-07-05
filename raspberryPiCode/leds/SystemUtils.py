
import psutil
from gpiozero import CPUTemperature
from gpiozero import LoadAverage
import os

class SystemUtils:

    @staticmethod
    def getCpuUsage() -> float:
        return round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2)

    @staticmethod
    def getMemoryUsage() -> float:
        return int(SystemUtils.mapToVals(int(psutil.virtual_memory().used/(1024*1024)), 0, int(psutil.virtual_memory().total/(1024*1024)), 0, 100))

    @staticmethod
    def getCpuTemp() -> float:
        return int(CPUTemperature().temperature)
    
    @staticmethod
    def mapToVals(x, in_min, in_max, out_min, out_max):
	    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min