import I2CBus


# JoystickController should manage all aspects of the joystick
class JoystickController:
    control_bus = None

    # These represent the commands used to get the states of the hardware

    # Vin1 = 0x10
    # Vin2 = 0x20
    # Vin3 = 0x30
    # Vin4 = 0x40

    last_resistor_position = None
    current_resistor_position = None

    resistor_address = None     # Vin1
    button_1_address = None     # Vin2
    button_2_address = None     # Vin3

    resistor_position = None
    button_1_pressed = None
    button_2_pressed = None

    def __init__(self):
        self.control_bus = I2CBus.I2CBus(0x21)

        self.resistor_address = 0x10
        self.button_1_address = 0x20
        self.button_2_address = 0x30

        self.resistor_position = self.get_resistor_position()
        self.button_1_pressed = False
        self.button_2_pressed = False

    def update(self):
        self.last_resistor_position = self.current_resistor_position
        self.current_resistor_position = self.get_resistor_position()

    def get_resistor_position(self):
        if self.control_bus is not None:
            if self.control_bus.is_bus_open():
                self.control_bus.set_command(self.resistor_address)    # Set command to the right pins
                pos = self.control_bus.read()
                return I2CBus.swap_high_low_byte(pos)
        return None

    def get_delta_resistor_position(self):
        if abs(self.last_resistor_position - self.current_resistor_position) > 10:
            if self.current_resistor_position < self.last_resistor_position:
                return 1
            elif self.current_resistor_position > self.last_resistor_position:
                return -1
        return 0
