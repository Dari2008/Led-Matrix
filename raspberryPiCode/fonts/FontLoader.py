from PIL import ImageFont

class FontLoader:
    @staticmethod
    def getFontPath(name: str, style: str="regular"):
        return f"./fonts/{name}-{style}.ttf"
    
    @staticmethod
    def loadFont(name: str, size: int, style: str="regular"):
        return ImageFont.truetype(FontLoader.getFontPath(name, style), size)