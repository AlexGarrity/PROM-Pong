import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

leds = [21, 22, 26, 23, 27, 24, 28, 25]

num = 0

for i in leds:
    GPIO.setup(i, GPIO.OUT)

while True:
    num += 1
    tempNum = num
    for i in range(8, 0, -1):
        if tempNum - (2 ** i) >= 0:
            print(str(tempNum) + " is bigger than or equal tdo " + str(2 ** i))
            GPIO.output(leds[i - 1], True)
            tempNum -= (2 ** i)
        else:
            print(str(tempNum) + " is smaller than " + str(2 ** i))
            GPIO.output(leds[i - 1], False)
    time.sleep(1)
