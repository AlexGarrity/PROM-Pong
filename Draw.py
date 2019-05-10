import SerialBus
import GPIO
import I2CBus
import Constants


class BoardPiece:
    BAT = 1
    BALL = 2
    TEXT = 3
    NET = 4


class Board:
    serial_bus = SerialBus.SerialBus()
    GPIO.init()

    # Stuff for LEDS
    i2c_controller = I2CBus.I2CBus(Constants.led_address)
    leds = [5, 6, 12, 13, 16, 19, 20, 26]
    pins = [254, 253, 251, 247, 239, 223, 191, 127, 255]

    # I didn't do anything to do with hit detection/locations of bats yet. I figured the game logic should go elsewhere.
    _board = [[]]
    _lastBoard = [[]]
    _length = 80
    _height = 24
    _ballX = 0
    _ballY = 0
    _playerOneBig = False
    _playerTwoBig = False
    # The pixels that are filled in the 3x5 space our numbers take.
    _numbers = {
        0:
            [0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 13, 14],
        1:
            [1, 4, 7, 10, 13],
        2:
            [0, 1, 2, 5, 6, 7, 8, 9, 12, 13, 14],
        3:
            [0, 1, 2, 5, 6, 7, 8, 11, 12, 13, 14],
        4:
            [0, 2, 3, 5, 6, 7, 8, 11, 14],
        5:
            [0, 1, 2, 3, 6, 7, 8, 11, 12, 13, 14],
        6:
            [0, 1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 14],
        7:
            [0, 1, 2, 3, 5, 8, 11, 14],
        8:
            [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14],
        9:
            [0, 1, 2, 3, 5, 6, 7, 8, 11, 14]
    }
    # hardcoded positions. too difficult to scale lettering to really small game dimensions
    _letters = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 2], [5, 1], [6, 2], [7, 3], [8, 2],
                [9, 1], [10, 0], [12, 0], [12, 1], [12, 2], [12, 3], [13, 0], [13, 3],
                [14, 0], [14, 3], [15, 0], [15, 1], [15, 2], [15, 3], [17, 0], [17, 1],
                [17, 2], [17, 3], [18, 1], [19, 2], [20, 0], [20, 1], [20, 2], [20, 3]]

    def __init__(self, length, height):



        for i in self.leds:
            GPIO.add_channel(i, True)

        self._length = length
        self._height = height
        self.full_clear()
        self.prepare()
        self.clearLastBoard(False)

    # Create our output for the console to print out
    def draw(self):
        for y in range(self._height):
            for x in range(self._length):
                if self._board[y][x] != self._lastBoard[y][x]:
                    if self._board[y][x]:
                        piece_color = self._board[y][x]
                        self.set_background_from_position(piece_color)
                        self.serial_bus.write_to_position(" ", y, x)
                    else:
                        self.serial_bus.set_background_color(SerialBus.Color.BLACK)
                        self.serial_bus.write_to_position(" ", y, x)
        self._lastBoard = self._board
        self.serial_bus.set_cursor_position(self._ballY, self._ballX)

    def set_background_from_position(self, piece_color):
        if piece_color == BoardPiece.NET:
            self.serial_bus.set_background_color(SerialBus.Color.BLUE)
        elif piece_color == BoardPiece.TEXT:
            self.serial_bus.set_background_color(SerialBus.Color.GREEN)
        elif piece_color == BoardPiece.BAT:
            self.serial_bus.set_background_color(SerialBus.Color.RED)
        elif piece_color == BoardPiece.BALL:
            self.serial_bus.set_background_color(SerialBus.Color.WHITE)
        else:
            self.serial_bus.set_background_color(SerialBus.Color.BLACK)

    def full_clear(self):
        self._board = [[False] * self._length for _ in range(self._height)]
        self._lastBoard = [[True] * self._length for _ in range(self._height)]
        self.draw()

    # Set our board to be completely empty
    def clear(self):
        self._board = [[False] * self._length for _ in range(self._height)]

    def clearScreen(self, value):
        self.clear()
        self.clearLastBoard(value)
        self.draw()

    def clearLastBoard(self, value):
        if value is not None:
            self._lastBoard = [[value] * self._length for _ in range(self._height)]

    # Initialise our board
    def new(self):

        # Net in middle of board.
        for iterator in range(2, self._height, 4):
            self._board[iterator][self._length // 2] = BoardPiece.NET
            if iterator + 1 != self._height:
                self._board[iterator + 1][self._length // 2] = BoardPiece.NET

    # We're using both commands anyways (usually. maybe we might want to just clear like in init),
    # so might as well merge.
    def prepare(self):
        self.clear()
        self.new()

    def draw_score(self, player_two, num):
        # Our offset positions for x and y.
        # Offsets are set in stone, always gonna be from the half-way point - 11, or + 8
        x_offset = (self._length // 2) + 8 if player_two else (self._length // 2) - 11
        y_offset = 1
        for pixel in range(15):
            x = pixel % 3
            y = pixel // 3
            self._board[y + y_offset][x + x_offset] = BoardPiece.TEXT and pixel in self._numbers[num] or False

    def updateScore(self, num, player_two=False):
        try:
            num = int(num)
        except ValueError:
            print("Number to be drawn is not valid")

        # We can change this later
        if not 0 <= num <= 9:
            num = 9

        self.draw_score(player_two, num)


    # debated func should just update a single bat, but decided on it updating both.
    # Reasoning is most likely both bats will change pos at same time
    # So it's just easier to not have to call this function twice (like we do for score)
    def updateBats(self, player_one_pos, player_two_pos, player_one_big, player_two_big):
        # Clear entire columns first.
        # useless var here but it looks nicer
        player_one_bat_x = 2
        player_two_bat_x = self._length - 3
        for y in range(self._height):
            self._board[y][player_one_bat_x] = False
            self._board[y][player_two_bat_x] = False

        # Could check if our midpoint is outside the game, but we do this in the game logic.

        # colour the pixels our bats should be in
        self._board[player_one_pos - 1][player_one_bat_x] = BoardPiece.BAT
        self._board[player_one_pos][player_one_bat_x] = BoardPiece.BAT
        self._board[player_one_pos + 1][player_one_bat_x] = BoardPiece.BAT
        if player_one_big:
            self._board[player_one_pos - 2][player_one_bat_x] = BoardPiece.BAT
            self._board[player_one_pos + 2][player_one_bat_x] = BoardPiece.BAT
            self._board[player_one_pos + 3][player_one_bat_x] = BoardPiece.BAT

        self._board[player_two_pos - 1][player_two_bat_x] = BoardPiece.BAT
        self._board[player_two_pos][player_two_bat_x] = BoardPiece.BAT
        self._board[player_two_pos + 1][player_two_bat_x] = BoardPiece.BAT
        if player_two_big:
            self._board[player_two_pos - 2][player_two_bat_x] = BoardPiece.BAT
            self._board[player_two_pos + 2][player_two_bat_x] = BoardPiece.BAT
            self._board[player_two_pos + 3][player_two_bat_x] = BoardPiece.BAT

    # draw our ball.  Ball could be in any position, so we can't just clear
    # the previous pos in case we destroy the net/scores
    # Solution: every tickrate, main code will clear -> initialise board -> update score -> update bats -> update ball.
    # Not optimal but isn't slow.

    # Deprecated in favour of storing previous board and only updating what changes

    def updateBall(self, x, y):
        self._ballX = x
        self._ballY = y

        # Update our GPIO LED depending on where the ball is. We can just clear every led first since
        # we dont know the last pos of the ball and this is easy

        for i in self.leds:
            GPIO.set_channel_status(i, False)

        # could have checked board length. didnt because we dont get marked on variable board size.
        ballpos = int(x / 10)

        GPIO.set_channel_status(self.leds[ballpos], True)
        self.i2c_controller.set_command(self.pins[ballpos])
        self.i2c_controller.write()

    def updateWinner(self, playerTwo=False):
        offsetX = 57 if playerTwo else 2
        offsetY = 4 if playerTwo else 1

        for position in self._letters:
            self._board[offsetY + position[1]][offsetX + position[0]] = BoardPiece.TEXT
