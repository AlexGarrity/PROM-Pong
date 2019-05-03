import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

leds = [5, 6, 12, 13, 16, 19, 20, 26]

num = 0

for i in leds:
    print("Setting up " + str(i))
    GPIO.setup(i, GPIO.OUT)
    print("Turning on " + str(i))
    GPIO.output(i, True)
    time.sleep(0.5)
    print("Turing off " + str(i))
    GPIO.output(i, False)
    time.sleep(1)


#basic adder
while True:
    num += 1
    tempNum = num
    for i in range(8, 0, -1):
        if tempNum - (2 ** i) >= 0:
            print(str(tempNum) + " is bigger than or equal to " + str(2 ** i))
            GPIO.output(leds[i - 1], True)
            tempNum -= (2 ** i)
        else:
            print(str(tempNum) + " is smaller than " + str(2 ** i))
            GPIO.output(leds[i - 1], False)
    time.sleep(0.25)
