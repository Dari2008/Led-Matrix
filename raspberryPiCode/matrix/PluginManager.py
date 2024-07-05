import matrix.Variables as Variables
import os
import json
from matrix.SettingsManager import SettingsManager

class PluginManager:

    @staticmethod
    def getConfig(pluginName: str):
        pluginDir = Variables.PLUGIN_DIR
        if(not os.path.exists(pluginDir + pluginName + "/config.json")):
            return None
        with open(pluginDir + pluginName + "/config.json", "r") as file:
            return json.load(file)
        
    @staticmethod
    def saveConfig(pluginName: str, config):
        if(config == None):
            return
        pluginDir = Variables.PLUGIN_DIR
        if(not os.path.exists(pluginDir + pluginName + "/")):
            return
        with open(pluginDir + pluginName + "/config.json", "w") as file:
            file.write(json.dumps(config))
            file.close()

    @staticmethod
    def addPlugin(pluginDirName: str):
        pluginDir = Variables.PLUGIN_DIR
        __ini__File = pluginDir + "/__init__.py"
        with open(__ini__File, "a+") as f:
            f.write(f"from matrix.plugins.{pluginDirName} import {pluginDirName}\n")
            f.close()

    @staticmethod
    def removePlugin(pluginDirName: str):
        pluginDir = Variables.PLUGIN_DIR
        __ini__File = pluginDir + "/__init__.py"
        with open(__ini__File, "r") as f:
            lines = f.readlines()
            f.close()

        with open(__ini__File, "w") as f:
            for line in lines:
                if not pluginDirName in line:
                    f.write(line)
            f.close()

        SettingsManager.removePluginSettings(pluginDirName)
        
        return os.system(f"rm -r -f {Variables.PLUGIN_DIR}{pluginDirName}") == 0
    
    @staticmethod
    def getPluginDirFromName(pluginName: str):
        pluginDir = Variables.PLUGIN_DIR
        dirs = os.listdir(pluginDir)
        for i in range(len(dirs)):
            if(os.path.isdir(pluginDir + dirs[i])):
                if(dirs[i] == pluginName):
                    return dirs[i]
        return None