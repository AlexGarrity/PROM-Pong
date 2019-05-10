from serial import Serial


class Color:
    BLACK = 30
    RED = 31
    GREEN = 32
    BLUE = 34
    WHITE = 37


# Serial bus is used for displaying on the screen
class SerialBus:
    serial_bus = None

    def __init__(self):
        if self.serial_bus is None:
            self.create_bus()

    def create_bus(self):
        self.serial_bus = Serial("/dev/ttyAMA0", 115200)

    def is_bus_open(self):
        if self.serial_bus is None:
            return False
        if not self.serial_bus.isOpen():
            return False
        return True

    def write(self, data):
        if self.is_bus_open():
            self.serial_bus.write(bytes(data, "UTF-8"))

    def write_to_position(self, character, x, y):
        self.set_cursor_position(x, y)
        self.write(character)

    def write_line(self, data):
        if self.is_bus_open():
            self.serial_bus.write(bytes(str(data) + "\r\n"), "UTF-8")

    def clear_screen(self):
        self.set_cursor_position(0, 0)
        self.write(chr(27) + "c")

    def new_line(self):
        self.write_line("")

    def set_cursor_position(self, x_position, y_position):
        self.write(chr(27) + "[%s;%sH" % (x_position + 1, y_position + 1))

    def set_foreground_color(self, color):
        self.write(chr(27) + "[" + str(color) + ";0m")

    def set_background_color(self, color):
        self.write(chr(27) + "[0;" + str(color + 10) + "m")
