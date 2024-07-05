from matrix.PluginManager import PluginManager
from matrix.SettingsManager import SettingsManager

class Plugin:

    def setSetting(self, key, value):
        SettingsManager.savePluginSettingsValue(self.PLUGIN_NAME, key, value)

    def getSetting(self, key, default=None):
        return SettingsManager.getPluginSettingsValue(self.PLUGIN_NAME, key, default)
    
    def getSettings(self):
        return SettingsManager.getPluginSettings(self.PLUGIN_NAME)
    
    def getSettingKeys(self):
        self.reloadConfig()
        return self.CONFIG["settingsKeys"]

    def reloadConfig(self):
        self.CONFIG = PluginManager.getConfig(self.PLUGIN_NAME)

    def setConfig(self, config):
        self.CONFIG = config

    def getConfig(self):
        return self.CONFIG
    
    def set(self, key, value):
        if(self.CONFIG == None):
            self.CONFIG = {}
        if(key == None):
            return
        if(value == None):
            if key in self.CONFIG:
                del self.CONFIG[key]
        print(f"Setting {key} to {value}")
        self.CONFIG[key] = value
        self.saveConfig()

    def get(self, key, default=None):
        return self.CONFIG[key] if key in self.CONFIG else default

    def saveConfig(self):
        PluginManager.saveConfig(self.PLUGIN_NAME, self.CONFIG)


    START = None
    STOP = None
    ON_PLUGIN_BTN_RELEASED = None
    ON_PLUGIN_BTN_PRESSED = None
    CONFIG = None
    PLUGIN_NAME = None
    MAIN_HOT_KEY_QUEUE = None