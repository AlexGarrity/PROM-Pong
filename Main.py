
import I2CBus
import SerialBus
import JoystickController

import time

if __name__ == "__main__":

    serial_bus = SerialBus.SerialBus()
    ic2_bus = I2CBus.I2CBus(0x21)
    joystick_controller = JoystickController.JoystickController()

    while True:
        last_position = None
        current_position = joystick_controller.get_resistor_position()
        if current_position is not None:
            if current_position != last_position:
                serial_bus.set_cursor_position(5, 5)
                serial_bus.write_line("Current resistor position: " + str(current_position))
                last_position = current_position
        else:
            serial_bus.write_line("Could not read resistor position")
        time.sleep(0.1)
