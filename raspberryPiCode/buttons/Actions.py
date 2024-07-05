from gpiozero import Button as Button

class Actions:
    def __init__(self) -> None:
        self.btn_picture = Button(Actions.BTN_IMAGE_PIN, hold_time=1, pull_up=True, bounce_time=0.2)
        self.btn_animation = Button(Actions.BTN_GIF_PIN, hold_time=1, pull_up=True, bounce_time=0.2)
        self.btn_plugin = Button(Actions.BTN_PLUGIN_PIN, hold_time=1, pull_up=True, bounce_time=0.2)
        self.btn_next = Button(Actions.BTN_NEXT_PIN, hold_time=1, pull_up=True, bounce_time=0.2)

        self.btn_picture.when_pressed = self.onPictureBtnPress
        self.btn_animation.when_pressed = self.onAnimationBtnPress
        self.btn_plugin.when_pressed = self.onPluginBtnPress
        self.btn_next.when_pressed = self.onNextBtnPress

        self.btn_plugin.when_released = self.onPluginBtnRelease
        self.btn_next.when_released = self.onNextBtnRelease
        self.btn_picture.when_released = self.onPictureBtnRelease
        self.btn_animation.when_released = self.onAnimationBtnRelease

        self.btn_next.when_held = self.onNextBtnHold
        self.btn_picture.when_held = self.onPictureBtnHold
        self.btn_animation.when_held = self.onAnimationBtnHold
        self.btn_plugin.when_held = self.onPluginBtnHold

    ON_PICTURE_BTN_REALEASE = []
    ON_ANIMATION_BTN_REALEASE = []
    ON_PLUGIN_BTN_REALEASE = []
    ON_NEXT_BTN_REALEASE = []

    ON_PICTURE_BTN_PRESS = []
    ON_ANIMATION_BTN_PRESS = []
    ON_PLUGIN_BTN_PRESS = []
    ON_NEXT_BTN_PRESS = []

    ON_PICTURE_BTN_HOLD = []
    ON_ANIMATION_BTN_HOLD = []
    ON_PLUGIN_BTN_HOLD = []
    ON_NEXT_BTN_HOLD = []

    def addOnPictureBtnRelease(self, func: callable):
        self.ON_PICTURE_BTN_REALEASE.append(func)

    def addOnAnimationBtnRelease(self, func: callable):
        self.ON_ANIMATION_BTN_REALEASE.append(func)

    def addOnPictureBtnPress(self, func: callable):
        self.ON_PICTURE_BTN_PRESS.append(func)

    def addOnAnimationBtnPress(self, func: callable):
        self.ON_ANIMATION_BTN_PRESS.append(func)

    def addOnPluginBtnPress(self, func: callable):
        self.ON_PLUGIN_BTN_PRESS.append(func)

    def addOnNextBtnPress(self, func: callable):
        self.ON_NEXT_BTN_PRESS.append(func)

    def addOnPluginBtnRelease(self, func: callable):
        self.ON_PLUGIN_BTN_REALEASE.append(func)

    def addOnNextBtnRelease(self, func: callable):
        self.ON_NEXT_BTN_REALEASE.append(func)

    def addOnNextBtnHold(self, func: callable):
        self.ON_NEXT_BTN_HOLD.append(func)

    def addOnPictureBtnHold(self, func: callable):
        self.ON_PICTURE_BTN_HOLD.append(func)

    def addOnAnimationBtnHold(self, func: callable):
        self.ON_ANIMATION_BTN_HOLD.append(func)

    def addOnPluginBtnHold(self, func: callable):
        self.ON_PLUGIN_BTN_HOLD.append(func)


    def onPictureBtnRelease(self):
        for func in self.ON_PICTURE_BTN_REALEASE:
            func()

    def onAnimationBtnRelease(self):
        for func in self.ON_ANIMATION_BTN_REALEASE:
            func()

    def onPictureBtnPress(self):
        for func in self.ON_PICTURE_BTN_PRESS:
            func()

    def onAnimationBtnPress(self):
        for func in self.ON_ANIMATION_BTN_PRESS:
            func()

    def onPluginBtnPress(self):
        for func in self.ON_PLUGIN_BTN_PRESS:
            func()

    def onNextBtnPress(self):
        for func in self.ON_NEXT_BTN_PRESS:
            func()

    def onPluginBtnRelease(self):
        for func in self.ON_PLUGIN_BTN_REALEASE:
            func()

    def onNextBtnRelease(self):
        for func in self.ON_NEXT_BTN_REALEASE:
            func()

    def onNextBtnHold(self):
        for func in self.ON_NEXT_BTN_HOLD:
            func()

    def onPictureBtnHold(self):
        for func in self.ON_PICTURE_BTN_HOLD:
            func()

    def onAnimationBtnHold(self):
        for func in self.ON_ANIMATION_BTN_HOLD:
            func()

    def onPluginBtnHold(self):
        for func in self.ON_PLUGIN_BTN_HOLD:
            func()

    def getBtnPicture(self) -> Button:
        return self.btn_picture
    
    def getBtnAnimation(self) -> Button:
        return self.btn_animation
    
    def getBtnPlugin(self) -> Button:
        return self.btn_plugin
    
    def getBtnNext(self) -> Button:
        return self.btn_next
    
    def getBtns(self) -> list:
        return [self.btn_picture, self.btn_animation, self.btn_plugin, self.btn_next]
    
    def remove(self, btnName: str, type: str, func):
        if(isinstance(func, int)):
            getattr(self, f"ON_" + btnName.upper() + "_BTN_" + type.upper()).pop(func)
        else:
            getattr(self, f"ON_" + btnName.upper() + "_BTN_" + type.upper()).remove(func)
    
    def getBtnsDict(self) -> dict:
        return {
            "picture": self.btn_picture,
            "animation": self.btn_animation,
            "plugin": self.btn_plugin,
            "next": self.btn_next
        }
    
    def getBtnsDictReversed(self) -> dict:
        return {
            self.btn_picture: "picture",
            self.btn_animation: "animation",
            self.btn_plugin: "plugin",
            self.btn_next: "next"
        }
    
    BTN_IMAGE_PIN = 26
    BTN_PLUGIN_PIN = 16
    BTN_GIF_PIN = 2
    BTN_NEXT_PIN = 3