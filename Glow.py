from PyGlow import PyGlow


import time
glow = PyGlow()
leds = [["white", 0], ["blue", 0], ["green", 0], ["yellow", 0], ["orange", 0], ["red", 0]]
order = [1, 3, 7, 15, 31, 63, 62, 60, 56, 48, 32, 0]


def score():
    for turn in order:
        for led in range(6):
            if turn & led == led:
                print("Turning on " + leds[led][0])
                leds[led][1] += int(255 / 20)
            else:
                print("Turning off " + leds[led][0])
                leds[led][1] = 0
            glow.color(leds[led][0], leds[led][1])
        time.sleep(0.125)

    for led in range(6):
        leds[led][1] = 0
        glow.color(leds[led][0], leds[led][1])

