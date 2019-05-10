import I2CBus
import GPIO
import Constants
import Debouncer

from math import log


import Constants


# JoystickController should manage all aspects of the joystick
class JoystickController:
    control_bus = None
    debouncer = None
    sw_debounce = False

    # These represent the commands used to get the states of the hardware

    # Vin1 = 0x10
    # Vin2 = 0x20
    # Vin3 = 0x30
    # Vin4 = 0x40

    last_resistor_position = 0
    current_resistor_position = 0

    resistor_address = [Constants.resistor_address, Constants.resistor_code]     # Vin1
    button_1_address = [Constants.button_address, Constants.button_code_11]     # Vin2
    button_2_address = [Constants.button_address, Constants.button_code_12]     # Vin3

    resistor_position = None
    button_1_pressed = None
    button_2_pressed = None

    voltage_interval = 4092 // Constants.height

    def __init__(self, resistor_channel, button_1_gpio, button_2_gpio, sw_debounce):
        self.control_bus = I2CBus.I2CBus(0x21)
        self.debouncer = Debouncer.Debouncer(0, 1, 0.4)
        self.sw_debounce = sw_debounce

        self.resistor_address = resistor_channel
        self.button_1_address = button_1_gpio
        self.button_2_address = button_2_gpio

        GPIO.add_channel(self.button_1_address, False)
        GPIO.add_channel(self.button_2_address, False)

        self.resistor_position = self.get_resistor_position()
        self.button_1_pressed = False
        self.button_2_pressed = False

    def update(self):
        self.last_resistor_position = self.current_resistor_position
        self.current_resistor_position = self.get_resistor_position()

        self.debouncer.update()
        self.get_button_state()

    def get_button_state(self):
            if self.sw_debounce:
                self.debouncer.set_signal(GPIO.get_channel_status(self.button_2_address))
                self.button_2_pressed = self.debouncer.get_state()
            else:
                self.button_2_pressed = GPIO.get_channel_status(self.button_2_address)
            self.button_1_pressed = GPIO.get_channel_status(self.button_1_address)

    def get_resistor_position(self):
        if self.control_bus is not None:
            if self.control_bus.is_bus_open():
                self.control_bus.set_command(self.resistor_address)    # Set command to the right pins
                self.current_resistor_position = self.control_bus.read()
                self.resistor_position = I2CBus.swap_high_low_byte(self.current_resistor_position)
                return self.resistor_position
        return None

    def get_resistor_screen_position(self):
        return self.resistor_position // self.voltage_interval
