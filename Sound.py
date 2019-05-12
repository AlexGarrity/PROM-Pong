import time
import RPi.GPIO as GPIO
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# default freq 100
GPIO.setup(11, GPIO.OUT)
PWM = GPIO.PWM(11, 100)
PWM.start(0)

mutex = threading.Lock()


class NoteSequence:
    notes = [[100, 0.1]]

    def __init__(self, notes):
        self.notes = notes


# Please don't look at this massive table of frequencies, it's ugly...
start_music = NoteSequence([
    [261.6,  0.5], [329.6,  0.5], [392.0,  0.5], [493.9,  0.5], [440.0,  0.5], [349.2,  0.5], [293.7,  0.5], [000.0,  0.5], [493.9,  0.5], [440.0,  0.5], [000.0,  3.0], 
    [329.6,  0.5], [392.0,  0.5], [587.3,  0.5], [493.9,  0.5], [392.0,  0.5], [349.2,  0.5], [293.7,  0.5], [000.0,  0.5], [329.6,  0.5], [392.0,  0.5], [000.0,  3.0], 
    [587.3,  0.5], [493.9,  0.5], [392.0,  0.5], [329.6,  0.5], [293.7,  0.5], [000.0,  0.5], [392.0,  0.5], [261.6,  0.5], [349.2,  0.5], [392.0,  0.5], [440.0,  0.5], [392.0,  0.5], [349.2,  0.5], [000.0,  1.5], 
    [440.0,  0.5], [493.9,  0.5], [440.0,  0.5], [392.0,  0.5], [329.6,  0.5], [293.7,  0.5], [349.2,  0.5], [000.0,  0.5], [523.3,  0.5], [440.0,  0.5], [000.0,  3.0], 
    [261.6,  0.5], [329.6,  0.5], [392.0,  0.5], [493.9,  0.5], [440.0,  0.5], [349.2,  0.5], [392.0,  0.5], [000.0,  0.5], [392.0,  0.5], [440.0,  0.5], [000.0,  3.0], 
    [587.3,  0.5], [493.9,  0.5], [329.6,  0.5], [392.0,  0.5], [293.7,  0.5], [349.2,  0.5], [392.0,  0.5], [000.0,  0.5], [392.0,  0.5], [329.6,  0.5], [000.0,  3.0], 
    [587.3,  0.5], [493.9,  0.5], [392.0,  0.5], [329.6,  0.5], [349.2,  0.5], [392.0,  0.5], [440.0,  0.5], [349.2,  0.5], [329.6,  0.5], [293.7,  0.5], [329.6,  0.5], [349.2,  0.5], [000.0,  1.5], 
    [440.0,  0.5], [493.9,  0.5], [440.0,  0.5], [392.0,  0.5], [329.6,  0.5], [293.7,  0.5], [349.2,  0.5], [440.0,  0.5], [261.6,  0.5], [000.0,  3.0]
])

hit_sequence = NoteSequence([[500, 0.1], [100, 0.1]])


def play_sequence(*args):
    mutex.acquire()
    PWM.ChangeDutyCycle(50)
    for note in args[0].notes:
        lock = threading.Lock()
        PWM.ChangeFrequency(note[0])
        time.sleep(note[1])
    PWM.ChangeDutyCycle(0)
    mutex.release()


def play_async(sequence: NoteSequence):
    thread = threading.Thread(None, play_sequence, None, sequence)
    thread.start()
    # Treat the thread as if it's detached from this point on
    # We don't need to tidy up, it only plays once
    # Also, it's Python.  I really don't care about performance
    # If it was C then maybe, but this isn't
    # To be fair, I don't even know if C has threading in stdlib
    # POSIX probably does
