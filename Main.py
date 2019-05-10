
import Pong
import GPIO

import JoystickController


# Can be used to initialise settings
def test_resistor():
    j = JoystickController.JoystickController()

    max_position = 0
    min_position = 1000

    while True:
        j.update()
        current_position = j.get_resistor_position()
        max_position = max(current_position, max_position)
        min_position = min(current_position, min_position)

        print("%e\t%e\t%e\t - %i" %
              (min_position, j.get_resistor_position(), max_position, j.get_resistor_screen_position()))


if __name__ == "__main__":
    application = Pong.Pong()
    application.start()
