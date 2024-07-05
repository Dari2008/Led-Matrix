from threading import Thread
from matrix.Plugin import Plugin
from matrix import Variables as Variables
import time
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from fonts.FontLoader import FontLoader
import cairosvg



class Main:
    def __init__(self, plugin: Plugin) -> None:
        self.running = False
        self.isGameRunning = False
        Variables.MATRIX.defaultFont = lambda size: FontLoader.loadFont("Jura", size)
        self.updaterThread = Thread(target=self.updater, daemon=True)
        self.plugin = plugin
        self.lastImages = {}

    def updater(self):
        while self.running:
            data, allData = self.updateScore()
            self.draw(data, allData)
            time.sleep(5)

    def draw(self, data, allData):
        if not self.isGameRunning or data == None:
            nextGame = self.getNextGame(allData)
            Variables.MATRIX.clear()
            r = 255
            g = 255
            b = 255
            a = 255
            nextGameColored = nextGame["vs"].split(" - ")
            nextGameColored = "\u001B[32m" + nextGameColored[0] + "\u001B[00m - \u001B[32m" + nextGameColored[1] + "\u001B[00m"
            Variables.MATRIX.drawTextInLineCenterWithSize(1, 6, "No game running", 15, r, g, b, a)
            Variables.MATRIX.drawTextInLineCenterWithSize(3, 6, "Next game: " + nextGameColored, 10, r, g, b, a)
            Variables.MATRIX.drawTextInLineCenterWithSize(5, 6, "Start: \u001B[33m" + nextGame["dt"], 10, r, g, b, a)
            Variables.MATRIX.show()
            return
        
        team1 = data["team1"]
        team2 = data["team2"]
        
        Variables.MATRIX.clear()

        if(team1["teamName"] not in self.lastImages):
            self.lastImages[team1["teamName"]] = self.getImageFromName(team1["teamName"])

        if(team2["teamName"] not in self.lastImages):
            self.lastImages[team2["teamName"]] = self.getImageFromName(team2["teamName"])

        team1Img = self.lastImages[team1["teamName"]]
        team2Img = self.lastImages[team2["teamName"]]

        imageMargin = 4

        Variables.MATRIX.drawImage(team1Img, 0, 0)
        Variables.MATRIX.drawImage(team2Img, Variables.MATRIX_WIDTH - team2Img.width, 0)

        Variables.MATRIX.drawRect(-1, -1, team1Img.width+1, team1Img.height+1, 255, 255, 255, 255)
        Variables.MATRIX.drawRect(Variables.MATRIX_WIDTH - team2Img.width - 1, -1, team2Img.width+1, team2Img.height+1, 255, 255, 255, 255)

        Variables.MATRIX.drawTextFloatLeft(team1["shortName"], team1Img.width+imageMargin, imageMargin, 255, 255, 255, 255)
        Variables.MATRIX.drawTextFloatRight(team2["shortName"], Variables.MATRIX_WIDTH - team2Img.width - imageMargin, imageMargin, 255, 255, 255, 255)

        count1 = data["matchResults"][0]["pointsTeam1"]
        count2 = data["matchResults"][0]["pointsTeam2"]

        colorlead = "\u001B[32m"
        colordraw = "\u001B[33m"
        colorloss = "\u001B[31m"

        color1 = ""
        color2 = ""

        if count1 > count2:
            color1 = colorlead
            color2 = colorloss
        elif count1 < count2:
            color1 = colorloss
            color2 = colorlead
        else:
            color1 = colordraw
            color2 = colordraw

        Variables.MATRIX.drawTextCenterCenterWithSize(color1 + str(data["matchResults"][0]["pointsTeam1"]) + "\u001B[00m - " + color2 + str(data["matchResults"][0]["pointsTeam2"]), 23, 255, 255, 255, 255)

        Variables.MATRIX.drawTextInLineCenterWithSize(3, 4, data["group"]["groupName"], 10, 255, 255, 255, 255)

        Variables.MATRIX.show()
        

    def getNextGame(self, allData):
        dateData = []

        for match in allData:
            dt = datetime.strptime(match["matchDateTime"].replace(r" ", ""), "%Y-%m-%dT%H:%M:%S")
            dateData.append({"date": dt, "title": match["team1"]["shortName"] + " - " + match["team2"]["shortName"]})

        dateData.sort(key=lambda x: x["date"])

        for data in dateData:
            if data["date"] > datetime.now():
                return {"vs": data["title"], "dt": data["date"].strftime("%H:%M")}

        return {"vs": "No game found", "dt": "?"}

    def getImageFromName(self, landName):
        extraCountries = {
            "Schottland": "gb-sct",
            "Wales": "gb-wls",
            "England": "gb-eng",
            "Polen": "pl",
            "Niederlande": "nl",
            "Slowenien": "si",
            # "Daenemark": "dk"
        }
        code = landName.lower()
        print(landName)
        if(landName not in extraCountries):
            url = f"https://restcountries.com/v3.1/name/{landName}"
            response = requests.get(url)
            data = response.json()
            if data is None or len(data) == 0:
                return None
            code = data[0]
            code = code.get("cca2", "").lower()
        else:
            landName = landName
            code = extraCountries[landName]

        print(code)

        url = f"https://flagcdn.com/h20/{code}.png"
        response = requests.get(url)
        return Image.open(BytesIO(response.content)).resize((25, 19))
        


    def updateScore(self):
        url = "https://api.openligadb.de/getmatchdata/em/2024/3"
        response = requests.get(url)
        matches = response.json()
        isOneRunning = False
        returner = None
        for match in matches:
            isRunning = not match["matchIsFinished"]
            dt = datetime.strptime(match["matchDateTime"].replace(r" ", ""), "%Y-%m-%dT%H:%M:%S")
            if isRunning and dt < datetime.now():
                isOneRunning = True
                returner = match
                return returner, matches

        self.isGameRunning = isOneRunning
        return returner, matches

    def start(self):
        self.running = True
        self.updaterThread.start()

    def stop(self):
        self.running = False
        self.updaterThread.join()
        self.score.reset()