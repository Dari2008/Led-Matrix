from matrix.Plugin import Plugin
from .Main import Main as EMScoreMain

class EMScore:

    def __init__(self, plugin: Plugin):
        plugin.START = self.start
        plugin.STOP = self.stop
        self.MAIN: EMScoreMain = EMScoreMain(plugin)

        
    def start(self):
        self.MAIN.start()

    def stop(self):
        self.MAIN.stop()