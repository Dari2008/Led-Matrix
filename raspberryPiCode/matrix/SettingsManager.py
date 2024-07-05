import json
import matrix.Variables as Variables
import os


class SettingsManager:

    @staticmethod
    def getPluginSettings(pluginName: str):
        if not os.path.exists(Variables.SETTINGS_DIR + pluginName + "_plugin.json"):
            return {}
        with open(Variables.SETTINGS_DIR + pluginName + "_plugin.json", "r") as file:
            return json.load(file)
        
    @staticmethod
    def savePluginSettings(pluginName: str, settings: dict):
        with open(Variables.SETTINGS_DIR + pluginName + "_plugin.json", "w") as file:
            json.dump(settings, file)

    @staticmethod
    def getPluginSettingsValue(pluginName: str, key: str, default=None):
        return SettingsManager.getPluginSettings(pluginName)[key] if key in SettingsManager.getPluginSettings(pluginName) else default
    
    @staticmethod
    def savePluginSettingsValue(pluginName: str, key: str, value):
        settings = SettingsManager.getPluginSettings(pluginName)
        settings[key] = value
        SettingsManager.savePluginSettings(pluginName, settings)

    @staticmethod
    def saveChangedPluginSettings(pluginName: str, settings: dict):
        currentSettings = SettingsManager.getPluginSettings(pluginName)
        for key in settings:
            currentSettings[key] = settings[key]
        SettingsManager.savePluginSettings(pluginName, currentSettings)

    @staticmethod
    def getImageSettings(imgName: str):
        if not os.path.exists(Variables.SETTINGS_DIR + imgName + "_image.json"):
            return {}
        with open(Variables.SETTINGS_DIR + imgName + "_image.json", "r") as file:
            return json.load(file)
        
    @staticmethod
    def saveImageSettings(imgName: str, settings: dict):
        with open(Variables.SETTINGS_DIR + imgName + "_image.json", "w") as file:
            json.dump(settings, file)

    @staticmethod
    def getImageSettingsValue(imgName: str, key: str):
        return SettingsManager.getImageSettings(imgName)[key]
    
    @staticmethod
    def saveImageSettingsValue(imgName: str, key: str, value):
        settings = SettingsManager.getImageSettings(imgName)
        settings[key] = value
        SettingsManager.saveImageSettings(imgName, settings)

    @staticmethod
    def saveChangedImageSettings(imgName: str, settings: dict):
        currentSettings = SettingsManager.getImageSettings(imgName)
        for key in settings:
            currentSettings[key] = settings[key]
        SettingsManager.saveImageSettings(imgName, currentSettings)

    @staticmethod
    def getGifSettings(gifName: str):
        if not os.path.exists(Variables.SETTINGS_DIR + gifName + "_gif.json"):
            return {}
        with open(Variables.SETTINGS_DIR + gifName + "_gif.json", "r") as file:
            return json.load(file)
        
    @staticmethod
    def saveGifSettings(gifName: str, settings: dict):
        with open(Variables.SETTINGS_DIR + gifName + "_gif.json", "w") as file:
            json.dump(settings, file)

    @staticmethod
    def getGifSettingsValue(gifName: str, key: str):
        return SettingsManager.getGifSettings(gifName)[key]
    
    @staticmethod
    def saveGifSettingsValue(gifName: str, key: str, value):
        settings = SettingsManager.getGifSettings(gifName)
        settings[key] = value
        SettingsManager.saveGifSettings(gifName, settings)

    @staticmethod
    def saveChangedGifSettings(gifName: str, settings: dict):
        currentSettings = SettingsManager.getGifSettings(gifName)
        for key in settings:
            currentSettings[key] = settings[key]
        SettingsManager.saveGifSettings(gifName, currentSettings)

    @staticmethod
    def getSettings():
        if not os.path.exists(Variables.SETTINGS_DIR + "settings.json"):
            return {}
        with open(Variables.SETTINGS_DIR + "settings.json", "r") as file:
            return json.load(file)
        
    @staticmethod
    def saveSettings(settings: dict):
        with open(Variables.SETTINGS_DIR + "settings.json", "w") as file:
            json.dump(settings, file)

    @staticmethod
    def getSettingsValue(key: str):
        return SettingsManager.getSettings()[key]
    
    @staticmethod
    def saveSettingsValue(key: str, value):
        settings = SettingsManager.getSettings()
        settings[key] = value
        SettingsManager.saveSettings(settings)

    @staticmethod
    def saveChangedSettings(settings: dict):
        currentSettings = SettingsManager.getSettings()
        for key in settings:
            currentSettings[key] = settings[key]
        SettingsManager.saveSettings(currentSettings)

    @staticmethod
    def removePluginSettings(pluginName: str):
        if os.path.exists(Variables.SETTINGS_DIR + pluginName + "_plugin.json"):
            os.remove(Variables.SETTINGS_DIR + pluginName + "_plugin.json")

    @staticmethod
    def removeImageSettings(imgName: str):
        if os.path.exists(Variables.SETTINGS_DIR + imgName + "_image.json"):
            os.remove(Variables.SETTINGS_DIR + imgName + "_image.json")

    @staticmethod
    def removeGifSettings(gifName: str):
        if os.path.exists(Variables.SETTINGS_DIR + gifName + "_gif.json"):
            os.remove(Variables.SETTINGS_DIR + gifName + "_gif.json")