import matrix.Server as Server
from matrix.MatrixClass import MatrixClass
import matrix.Variables as Variables
import sys
import os
from PIL import GifImagePlugin
GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

def addPath():
    path = os.path.abspath("plugins")
    sys.path.append(path)

def init():
    Server.initServer()

def run():
    addPath()
    Variables.MATRIX = MatrixClass()
    Server.start()
    print("Server stopped")

def clear():
    Variables.MATRIX.clear()
    Variables.MATRIX.show()
    Server.clear()
    print("Matrix cleared")