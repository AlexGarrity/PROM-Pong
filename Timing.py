import time


class Timing:
    lastTime = 0
    currentTime = 0
    deltaTime = 0
    # It runs on a console, and console players can't see over 30FPS anyway, so 33ms will do...
    timePerFrame = 16
    timeToNextFrame = 0

    def __init__(self):
        self.lastTime = time.time()
        self.deltaTime = self.lastTime

    def update_time(self):
        self.currentTime = time.time()
        self.deltaTime = self.currentTime - self.lastTime
        self.lastTime = self.currentTime

    def wait_for_update(self):
        self.timeToNextFrame = self.timePerFrame - self.deltaTime
        if self.timeToNextFrame > 0:
            time.sleep(self.timeToNextFrame / 1000)
