import time
import RPi.GPIO as GPIO
from random import randrange

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# default freq 100
GPIO.setup(11, GPIO.OUT)
PWM = GPIO.PWM(11, 100)
PWM.start(0)

# I have no idea if this would even sound good
def reset():
    PWM.ChangeDutyCycle(0)
    PWM.ChangeFrequency(100)


def start():
    PWM.ChangeDutyCycle(50)
    PWM.ChangeFrequency(100)
    time.sleep(0.4)
    PWM.ChangeFrequency(200)
    time.sleep(0.4)
    PWM.ChangeFrequency(400)
    time.sleep(0.4)
    PWM.ChangeFrequency(300)
    time.sleep(0.4)
    PWM.ChangeFrequency(500)
    time.sleep(0.4)
    reset()


def hit():
    PWM.ChangeDutyCycle(50)
    freq = randrange(100, 600)
    PWM.ChangeFrequency(100)
    PWM.ChangeFrequency(freq)
    time.sleep(0.1)
    reset()


