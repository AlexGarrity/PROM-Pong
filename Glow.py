from PyGlow import PyGlow


import time
glow = PyGlow()
leds = [["White", 0], ["Blue", 0], ["Green", 0], ["Yellow", 0], ["Orange", 0], ["Red", 0]]
order = [1, 3, 7, 15, 31, 63, 62, 60, 56, 48, 32, 0]


def score():
    for turn in order:
        for led in range(7):
            if turn & led == led:
                print("Turning on " + leds[led][0])
                leds[led][1] += int(255 / 6)
            else:
                print("Turning off " + leds[led][0])
                leds[led][1] = 0
            glow.color(leds[led][0], leds[led][1])
        time.sleep(0.25)
