
import RPi.GPIO as gpio


# Pretty much just a wrapper for RPi.GPIO

channels_in_use = []


def init():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)


def add_channel(channel_number, output):
    if channel_number not in channels_in_use:
        channels_in_use.append(channel_number)
        if output:
            gpio.setup(channel_number, gpio.OUT)
        else:
            gpio.setup(channel_number, gpio.IN)


def remove_channel(channel_number):
    if channel_number in channels_in_use:
        channels_in_use.remove(channel_number)
        gpio.cleanup(channel_number)


def get_channel_status(channel_number):
    if channel_number in channels_in_use:
        return gpio.input(channel_number)


def set_channel_status(channel_number, state):
    if channel_number in channels_in_use:
        gpio.output(channel_number, state)


