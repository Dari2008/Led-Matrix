from gpiozero import Button as Button
import time

BTN_IMAGE_PIN1 = 26
BTN_IMAGE_PIN2 = 16
BTN_IMAGE_PIN3 = 2
BTN_IMAGE_PIN4 = 3
IMAGE = 26
PLUGIN = 16
NEXT = 3
GIF = 2

def onPin(pinNum):
    print(f"Pin {pinNum} pressed")


btn1 = Button(BTN_IMAGE_PIN1, hold_time=1, pull_up=True, bounce_time=0.2)
btn2 = Button(BTN_IMAGE_PIN2, hold_time=1, pull_up=True, bounce_time=0.2)
btn3 = Button(BTN_IMAGE_PIN3, hold_time=1, pull_up=True, bounce_time=0.2)
btn4 = Button(BTN_IMAGE_PIN4, hold_time=1, pull_up=True, bounce_time=0.2)

btn1.when_held = lambda: onPin(BTN_IMAGE_PIN1)
btn2.when_held = lambda: onPin(BTN_IMAGE_PIN2)
btn3.when_held = lambda: onPin(BTN_IMAGE_PIN3)
btn4.when_held = lambda: onPin(BTN_IMAGE_PIN4)

while True:
    time.sleep(1)