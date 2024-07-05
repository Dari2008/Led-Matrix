from matrix.Plugin import Plugin
from .Main import Main as PongMain
from . import Vars

class Pong:

    def __init__(self, plugin: Plugin):
        Vars.PLUGIN = plugin
        plugin.START = self.start
        plugin.STOP = self.stop
        self.MAIN: PongMain = PongMain()

        
    def start(self):
        self.MAIN.start()

    def stop(self):
        self.MAIN.stop()