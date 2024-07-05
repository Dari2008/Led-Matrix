import matrix.Variables as Variables
from matrix.Plugin import Plugin as Plugin

class TestPlugin:
    def __init__(self, plugin: Plugin):
        print("Plugin initialized")
        self.plugin = plugin
        self.plugin.START = self.start
        self.plugin.STOP = self.stop

    def start(self):
        print("Plugin started")

        for i in range(0, 10):
            Variables.MATRIX.setColor(i, 0, 255, 0, 0)
        Variables.MATRIX.show()
    
    def stop(self):
        print("Plugin stopped")

        for i in range(0, 10):
            Variables.MATRIX.setColor(i, 0, 0, 0, 0)
        Variables.MATRIX.show()