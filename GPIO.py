
import RPi.GPIO as gpio


# Pretty much just a wrapper for RPi.GPIO
class GPIOController:

    channels_in_use = []

    def __init__(self):
        gpio.setmode(gpio.board)
        gpio.setup(self.channels_in_use, gpio.out)

    def __del__(self):
        gpio.cleanup()

    def add_channel(self, channel_number):
        if channel_number not in self.channels_in_use:
            self.channels_in_use.append(channel_number)

    def remove_channel(self, channel_number):
        if channel_number in self.channels_in_use:
            self.channels_in_use.remove(channel_number)
            gpio.cleanup(channel_number)

    def get_channel_status(self, channel_number):
        if channel_number in self.channels_in_use:
            return gpio.input(channel_number)

    def set_channel_status(self, channel_number, state):
        if channel_number in self.channels_in_use:
            gpio.output(channel_number, state)
