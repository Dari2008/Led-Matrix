from twisted.internet import protocol, reactor, endpoints
from twisted.protocols.basic import LineOnlyReceiver
import json
import os
import base64
import zipfile

from matrix.GifLoader import GifLoader
from matrix.ImageLoader import ImageLoader
from matrix.PluginLoader import PluginLoader

from matrix.PluginManager import PluginManager
from matrix.SettingsManager import SettingsManager
from leds.BackgroundLedStrip import BackgroundLedStrip

import matrix.Variables as Variables

import sys

class Server(LineOnlyReceiver):
    MAX_LENGTH = sys.maxsize-100000

    def __init__(self):
        Variables.SERVER = self


    def lineReceived(self, data):
        data = data.decode("utf-8")
        self.processData(data)

    def processData(self, d):
        try:
            data = json.loads(d)
            action = data["action"]
            print("Action: ", action)
            if action == "loadImage":
                self.loadImage(data)
            elif action == "loadGif":
                self.loadGif(data)
            elif action == "loadPlugin":
                self.loadPlugin(data)
            elif action == "clear":
                self.clear()
            elif action == "getPlugins":
                self.getPlugins()
            elif action == "setBrightness":
                self.setBrightness(data)
            elif action == "getCurrentDisplay":
                self.getCurrentDisplay()
            elif action == "upload":
                self.upload(data)
            elif action == "deletePlugin":
                self.deletePlugin(data)
            elif action == "deleteImage":
                self.deleteImage(data)
            elif action == "deleteGif":
                self.deleteGif(data)
            elif action == "getPluginConfig":
                self.getPluginConfig(data)
            elif action == "savePluginConfig":
                self.savePluginConfig(data)
            elif action == "getImages":
                self.getImages()
            elif action == "getGifs":
                self.getGifs()
            elif action == "getAllData":
                self.getAllData()
            elif action == "editGif":
                self.editGif(data)
            elif action == "editImage":
                self.editImage(data)
            elif action == "editPlugin":
                self.editPlugin(data)
            else:
                self.send(self.toErrorJson("Action not found", ValueError("Action not found")))
                return
            
        except Exception as e:
            self.send(self.toErrorJson("Invalid JSON", e))
            return
        
    def editPlugin(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        if not "data" in data:
            self.send(self.toErrorJson("Config is missing", ValueError("<data> is missing")))
            return
        
        try:
            SettingsManager.saveChangedPluginSettings(data["name"], data["data"])
            self.sendSuccess()
        except Exception as e:
            self.send(self.toErrorJson("Error while editing plugin", e))
            return
        
    def editImage(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        if not "data" in data:
            self.send(self.toErrorJson("Data is missing", ValueError("<data> is missing")))
            return

        try:
            SettingsManager.saveChangedImageSettings(data["name"], data["data"])
            self.sendSuccess()
        except Exception as e:
            print(e)
            self.send(self.toErrorJson("Error while editing image", e))
            return

    def editGif(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        if not "data" in data:
            self.send(self.toErrorJson("Data is missing", ValueError("<data> is missing")))
            return

        try:
            SettingsManager.saveChangedGifSettings(data["name"], data["data"])
            self.sendSuccess()
        except Exception as e:
            print(e)
            self.send(self.toErrorJson("Error while editing gif", e))
            return
        
    def getAllData(self):
        try:
            images = ImageLoader.getImages()
            gifs = GifLoader.getGifs()
            plugins = PluginLoader.getPlugins()
            self.send({"images": images, "gifs": gifs, "plugins": plugins, "ok": True})
        except Exception as e:
            self.send(self.toErrorJson("Error while getting all data", e))
            return
    
    def getImages(self):
        try:
            images = ImageLoader.getImages()
            self.send({"images": images, "ok": True})
        except Exception as e:
            self.send(self.toErrorJson("Error while getting images", e))
            return
        
    def getGifs(self):
        try:
            gifs = GifLoader.getGifs()
            self.send({"gifs": gifs, "ok": True})
        except Exception as e:
            self.send(self.toErrorJson("Error while getting gifs", e))
            return
        
    def getPluginConfig(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        try:
            config = PluginManager.getConfig(data["name"])
            self.send({"config": config, "ok": True})
        except Exception as e:
            self.send(self.toErrorJson("Error while getting plugin config", e))
            return
        
    def deleteGif(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        try:
            success = GifLoader.removeGif(data["name"])
            if(not success["ok"]):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            else:
                self.send(success)
        except Exception as e:
            print(e)
            self.send(self.toErrorJson("Error while deleting gif", e))
            return
        
    def deleteImage(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        try:
            success = ImageLoader.removeImage(data["name"])
            if(not success["ok"]):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            else:
                self.send(success)
        except Exception as e:
            print(e)
            self.send(self.toErrorJson("Error while deleting image", e))
            return
        
    def deletePlugin(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        try:
            success = PluginLoader.removePlugin(data["name"])
            if(not success["ok"]):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            else:
                self.send(success)
        except Exception as e:
            self.send(self.toErrorJson("Error while deleting plugin", e))
            return
        
    def savePluginConfig(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        if not "config" in data:
            self.send(self.toErrorJson("Config is missing", ValueError("<config> is missing")))
            return
        
        try:
            success = PluginManager.saveConfig(data["name"], data["config"])
            if(not success["ok"]):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            else:
                self.send(success)
        except Exception as e:
            self.send(self.toErrorJson("Error while saving plugin config", e))
            return
        
    def getMime(self, extension):
        if extension == ".jpg" or extension == ".jpeg":
            return "image/jpeg"
        if extension == ".png":
            return "image/png"
        if extension == ".gif":
            return "image/gif"
        if extension == ".zip":
            return "application/zip"
        return "application/octet-stream"

    def upload(self, data):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("<name> is missing")))
            return
        
        if not "data" in data:
            self.send(self.toErrorJson("Data is missing", ValueError("<data> is missing")))
            return
        
        encryption = None

        if "encryption" in data:
            encryption = data["encryption"]

        if(encryption != None and encryption != "none" and encryption != "base64"):
            self.send(self.toErrorJson("Encryption not supported", ValueError("Encryption not supported")))
            return
        
        if(encryption == "base64"):
            data["data"] = base64.b64decode(data["data"].encode("utf-8"))
        else:
            data["data"] = data["data"].encode("utf-8")
        
        extension = os.path.splitext(data["name"])[1]
        try:
            if(extension == ".gif"):
                with open(f"{Variables.GIF_DIR}/{data['name']}", "wb") as f:
                    f.write(data["data"])
                    self.sendSuccess()
                return
            
            if(extension == ".zip"):
                with open(f"{Variables.TMP_DIR}{data['name']}", "wb") as f:
                    f.write(data["data"])

                success = PluginLoader.loadPluginFromZip(f"{Variables.TMP_DIR}{data['name']}", data['name'])
                if(not success["ok"]):
                    self.send(self.toErrorJson(success["msg"], success["e"]))
                    return
                else:
                    self.send(success)
                return
            
            if(extension == ".jpg" or extension == ".jpeg" or extension == ".png"):
                with open(f"{Variables.IMAGE_DIR}/{data['name']}", "wb") as f:
                    f.write(data["data"])
                    self.sendSuccess()
                return
        except Exception as e:
            print(e)
            self.send(self.toErrorJson("Error while uploading plugin", e))
            return
        
        
    def getCurrentDisplay(self):
        try:
            if(ImageLoader.isActive()):
                self.send({"type": "image", "data": {"name": Variables.LAST_USED_DATA["lastImagePath"]}, "ok": True})
            elif(GifLoader.isActive()):
                self.send({"type": "gif", "data": {"name": Variables.LAST_USED_DATA["lastGifPath"]}, "ok": True})
            elif(PluginLoader.isActive()):
                self.send({"type": "plugin", "data": {"name": Variables.LAST_USED_DATA["lastPlugin"]}, "ok": True})
            else:
                self.send({"type": "none", "ok": True})
        except Exception as e:
            self.send(self.toErrorJson("Error while getting current display", e))
            return
    
    def setBrightness(self, data):
        if not "brightness" in data:
            self.send(self.toErrorJson("Brightness is missing", ValueError("<brightness> is missing")))
            return
        
        try:
            Variables.MATRIX.setBrightness(data["brightness"])
            self.sendSuccess()
        except Exception as e:
            self.send(self.toErrorJson("Error while setting brightness", e))
            return
        
    def getPlugins(self):
        try:
            plugins = PluginLoader.getPlugins()
            self.send({"plugins": plugins, "ok": True})
        except Exception as e:
            self.send(self.toErrorJson("Error while getting plugins", e))
            return
        
    def loadImage(self, data, isSystem=False):
        if not "name" in data:
            self.send(self.toErrorJson("Path is missing", ValueError("<name> is missing")))
            return
        
        try:
            self.clear(True)
            success = ImageLoader.displayImage(data["name"])
            if(not success["ok"] and not isSystem):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            
            Variables.LAST_USED_DATA["lastImagePath"] = data["name"]
            Variables.saveLastUsedData()
            if(not isSystem):
                self.sendSuccess()
        except Exception as e:
            print(e)
            if(not isSystem):
                self.send(self.toErrorJson("Error while loading image", e))
            return

    def loadGif(self, data, isSystem=False):
        if not "name" in data:
            self.send(self.toErrorJson("Path is missing", ValueError("<name> is missing")))
            return
        
        try:
            self.clear(True)
            success = GifLoader.displayGif(data["name"])
            if(not success["ok"] and not isSystem):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            
            Variables.LAST_USED_DATA["lastGifPath"] = data["name"]
            Variables.saveLastUsedData()
            if(not isSystem):
                self.sendSuccess()
        except Exception as e:
            if(not isSystem):
                self.send(self.toErrorJson("Error while loading image", e))
            return

    def loadPlugin(self, data, isSystem=False):
        if not "name" in data:
            self.send(self.toErrorJson("Name is missing", ValueError("name is missing")))
            return
        try:
            self.clear(True)
            success = PluginLoader.loadPlugin(data["name"])
            if(not success["ok"] and not isSystem):
                self.send(self.toErrorJson(success["msg"], success["e"]))
                return
            
            Variables.LAST_USED_DATA["lastPluginPath"] = data["name"]
            Variables.saveLastUsedData()
            if(not isSystem):
                print("Sending success")
                self.sendSuccess()
        except Exception as e:
            if(not isSystem):
                self.send(self.toErrorJson("Error while loading plugin", e))
            return

    def clear(self=None, isProgrammatic = False):
        try:
            stopped = []
            responses = {}

            if(ImageLoader.isActive()):
                imageResponse = ImageLoader.hideImage()
                if(imageResponse["ok"]):
                    stopped.append("Image")
                responses["image"] = imageResponse

            if(GifLoader.isActive()):
                gifResponse = GifLoader.hideGif()
                if(gifResponse["ok"]):
                    stopped.append("Gif")
                responses["gif"] = gifResponse

            if(PluginLoader.isActive()):
                pluginResponse = PluginLoader.unloadPlugin()
                if(pluginResponse["ok"]):
                    stopped.append("Plugin")
                responses["plugin"] = pluginResponse

            BackgroundLedStrip.clearStrip()
            BackgroundLedStrip.show()
                

            Variables.MATRIX.createNewImage()
            Variables.MATRIX.show()

            if not isProgrammatic and self != None:
                self.send({"stopped": stopped, "responses": responses, "ok": True})
        except Exception as e:
            if not isProgrammatic and self != None:
                self.send(self.toErrorJson("Error while clearing", e))
            return
        
    def sendSuccess(self):
        self.send({"ok": True})

    def toErrorJson(self, msg, e: Exception = None) -> json:
        return {"message": msg, "error": e.__str__(), "ok": False}
    
    def send(self, data):
        self.transport.write((json.dumps(data) + "\n").encode("utf-8"))
        self.transport.loseConnection()

    def sendString(self, data, newLine = False):
        self.transport.write((data + ("\n" if newLine else "")).encode("utf-8"))
        self.transport.loseConnection()

class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Variables.SERVER
    

def initServer():
    Variables.SERVER = Server()

def start():
    endpoints.serverFromString(reactor, f"tcp:{Variables.MAIN_PORT}").listen(ServerFactory()).addCallback(lambda _: print("Server started"))
    reactor.run()
    GifLoader.hideGif()

def clear():
    Server.clear()