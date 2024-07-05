import os
import importlib as importlib
import sys
import threading
import zipfile
import json
import Main

from matrix.Plugin import Plugin as Plugin
import matrix.Variables as Variables
from matrix.PluginManager import PluginManager
from matrix.SettingsManager import SettingsManager

class PluginLoader:

    @staticmethod
    def loadPlugin(pluginName: str):
        try:
            (PluginLoader.CURRENT_PLUGIN, PluginLoader.CURRENT_CLASS_INSTANCE) = PluginLoader.factory(pluginName)
            threading.Thread(target=PluginLoader.CURRENT_PLUGIN.START, daemon=True).start()
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while loading plugin", "e": e}
                
    
    @staticmethod
    def unloadPlugin():
        if(PluginLoader.CURRENT_PLUGIN == None):
            return {"ok": False, "msg": "No plugin loaded"}
        try:
            t = threading.Thread(target=PluginLoader.CURRENT_PLUGIN.STOP, daemon=True)
            t.start()
            t.join()
            PluginLoader.CURRENT_PLUGIN = None
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while unloading plugin", "e": e}
        
    @staticmethod
    def isActive():
        return PluginLoader.CURRENT_PLUGIN != None
    
    @staticmethod
    def factory(pluginName: str, initialize: bool = True):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, script_directory)
        pluginDir = importlib.import_module(f'matrix.plugins')
        file = getattr(pluginDir, pluginName)
        class_ = getattr(file, pluginName)
        plugin = Plugin()
        plugin.CONFIG = PluginManager.getConfig(pluginName)
        plugin.PLUGIN_NAME = pluginName
        if(initialize):
            return (plugin, class_(plugin))
        return (class_)
    
    @staticmethod
    def loadPluginFromZip(zipPath: str, fileName: str):
        try:
            with zipfile.ZipFile(zipPath, 'r') as zip_ref:
                zip_ref.extractall(Variables.PLUGIN_DIR + fileName.replace(".zip", ""))
                zip_ref.close()
                os.system(f"rm {zipPath} -f")

            PluginManager.addPlugin(fileName.replace(".zip", ""))
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while loading plugin from zip", "e": e}

    @staticmethod
    def removePlugin(pluginName: str):
        try:
            dirName = PluginManager.getPluginDirFromName(pluginName)
            PluginManager.removePlugin(dirName)
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"ok": False, "msg": "Error while removing plugin", "e": e}
        
    @staticmethod
    def getPlugins():
        pluginDir = Variables.PLUGIN_DIR
        dirs = os.listdir(pluginDir)
        resultDirs = []
        for i in range(len(dirs)):
            if(os.path.isdir(pluginDir + dirs[i])):
                resultDirs.append(dirs[i])

        data = []
        for i in range(len(resultDirs)):
            if(resultDirs[i] == "__pycache__"):
                continue

            if(not os.path.exists(pluginDir + resultDirs[i] + "/config.json")):
                data.append({"name": resultDirs[i], "uploaded": os.path.getctime(pluginDir + resultDirs[i])})
                continue
            try:
                with open(pluginDir + resultDirs[i] + "/config.json", "r") as yaml_file:
                    config = json.load(yaml_file)
                    settings = []
                    settingsValues = SettingsManager.getPluginSettings(resultDirs[i])
                    settingsKeys = PluginLoader.getOrDefault(config, "settingsKeys", [])
                    settingsDefaults = PluginLoader.getOrDefault(config, "settingsDefaults", {})
                    desc = PluginLoader.getOrDefault(config, "description", "")
                    version = PluginLoader.getOrDefault(config, "version", "")

                    for key in settingsKeys:
                        if key not in settingsValues:
                            settingsValues[key] = ""

                    for key in settingsValues:
                        settings.append({
                            "name": key,
                            "value": settingsValues[key] if key in settingsValues else "",
                            "default": settingsDefaults[key] if key in settingsDefaults else ""
                        })

                    data.append({
                        "name": config["name"], 
                        "uploaded": os.path.getctime(pluginDir + resultDirs[i]),
                        "settings": settings,
                        "description": desc,
                        "version": version
                    })
            except Exception as e:
                data.append({
                    "name": resultDirs[i], 
                    "uploaded": os.path.getctime(pluginDir + resultDirs[i]), 
                    "exception": e.__str__()
                })
        return data
    
    @staticmethod
    def getOrDefault(settings, key, value):
        if key in settings:
            return settings[key]
        return value

    CURRENT_CLASS_INSTANCE = None
    CURRENT_PLUGIN: Plugin = None