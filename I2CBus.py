import smbus


# I2CBus is used for reading data from, and writing data to, hardware

# Helper function for swapping high and low bytes from the AD799
def swap_high_low_byte(data):
    return data >> 8 | (data & 0x00FF) << 8


class I2CBus:
    I2C_address = None
    I2C_command = None
    bus = None

    last_data = None

    def __init__(self, address):
        self.set_address(address)
        self.create_bus()

    def __del__(self):
        self.close_bus()

    def create_bus(self):
        if not self.is_bus_open():
            self.bus = smbus.SMBus(1)

    def close_bus(self):
        if self.is_bus_open():
            self.bus.close()

    def is_bus_open(self):
        if self.bus is not None:
            return True
        return False

    def set_address(self, address):
        self.I2C_address = address

    def set_command(self, command):
        if command > 0:
            self.I2C_command = command

    def read(self):
        if self.I2C_command is not None:
            if self.is_bus_open():
                self.bus.write_byte(self.I2C_address, self.I2C_command)
                self.last_data = self.bus.read_word_data(self.I2C_address, 0x00)
                return self.last_data
        return None

    def write(self, data):
        if self.I2C_command is not None:
            if self.is_bus_open():
                self.bus.write_byte_data(self.I2C_address, self.I2C_command, data)
