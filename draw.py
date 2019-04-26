import SerialBus


class Board():

    serial_bus = SerialBus.SerialBus()

    # I didn't do anything to do with hit detection/locations of bats yet. I figured the game logic should go elsewhere.
    _board = []
    _lastBoard = []
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
    _letters = [ [0, 0], [1, 1], [2, 2], [3, 3], [4, 2], [5, 1], [6, 2], [7, 3], [8, 2], 
                 [9, 1], [10, 0], [12, 0], [12, 1], [12, 2], [12, 3], [13, 0], [13, 3], 
                 [14, 0], [14, 3], [15, 0], [15, 1], [15, 2], [15, 3], [17, 0], [17, 1], 
                 [17, 2], [17, 3], [18, 1], [19, 2], [20, 0], [20, 1], [20, 2], [20, 3] ]

    def __init__(self, length, height):
        self._length = length
        self._height = height
        self.clear()
        self.clearLastBoard(False)

    # Create our output for the console to print out
    def draw(self):
        for y in range(self._height):
            for x in range(self._length):
                if self._board[y][x] != self._lastBoard[y][x]:
                    if self._board[y][x]:
                        self.serial_bus.set_background_color(SerialBus.Color.WHITE)
                        self.serial_bus.write_to_position(" ", y, x)
                    else:
                        self.serial_bus.set_background_color(SerialBus.Color.BLACK)
                        self.serial_bus.write_to_position(" ", y, x)
        self._lastBoard = self._board
        self.serial_bus.set_cursor_position(self._ballY, self._ballX)

    # Set our board to be completely empty
    def clear(self):
        self._board = [[False] * self._length for _ in range(self._height)]

    def clearScreen(self, value):
        self.clear()
        self.clearLastBoard(True)
        self.draw()

    def clearLastBoard(self, value):
        if value:
            self._lastBoard = [[value] * self._length for _ in range(self._height)]

    # Initialise our board
    def new(self):

        # Net in middle of board.
        for i in range(2, self._height, 4):
            self._board[i][self._length // 2] = True
            if i + 1 != self._height:
                self._board[i+1][self._length // 2] = True

    # We're using both commands anyways (usually. maybe we might want to just clear like in init),
    # so might as well merge.
    def prepare(self):
        self.clear()
        self.new()
        
    def updateScore(self, num, playerTwo = False):
        try:
            num = int(num)
        except ValueError:
            print("Number to be drawn is not valid")
    
        # We can change this later
        if not 0 <= num <= 9:
            num = 9

        # Our offset positions for x and y.
        # Offsets are set in stone, always gonna be from the half-way point - 11, or + 8
        xOffset = (self._length // 2) + 8 if playerTwo else (self._length // 2) - 11
        yOffset = 1

        for pixel in range(15):
            x = pixel % 3
            y = pixel // 3
            self._board[y + yOffset][x + xOffset] = True and pixel in self._numbers[num] or False

    # debated func should just update a single bat, but decided on it updating both.
    # Reasoning is most likely both bats will change pos at same time
    # So it's just easier to not have to call this function twice (like we do for score)
    def updateBats(self, playerOnePos, playerTwoPos, playerOneBig, playerTwoBig):
        # Clear entire columns first.
        # useless var here but it looks nicer
        playerOneBatX = 2
        playerTwoBatX = self._length - 3
        for y in range(self._height):
            self._board[y][playerOneBatX] = False
            self._board[y][playerTwoBatX] = False
            
        # Could check if our midpoint is outside the game, but we do this in the game logic.

        # colour the pixels our bats should be in
        self._board[playerOnePos - 1][playerOneBatX] = True
        self._board[playerOnePos][playerOneBatX] = True
        self._board[playerOnePos + 1][playerOneBatX] = True
        if playerOneBig:
            self._board[playerOnePos - 2][playerOneBatX] = True
            self._board[playerOnePos + 2][playerOneBatX] = True
            self._board[playerOnePos + 3][playerOneBatX] = True
            
        self._board[playerTwoPos - 1][playerTwoBatX] = True
        self._board[playerTwoPos][playerTwoBatX] = True
        self._board[playerTwoPos + 1][playerTwoBatX] = True
        if playerTwoBig:
            self._board[playerTwoPos - 2][playerTwoBatX] = True
            self._board[playerTwoPos + 2][playerTwoBatX] = True
            self._board[playerTwoPos + 3][playerTwoBatX] = True

    # draw our ball.  Ball could be in any position, so we can't just clear
    # the previous pos in case we destroy the net/scores
    # Solution: every tickrate, main code will clear -> initialise board -> update score -> update bats -> update ball.
    # Not optimal but isn't slow.

    def updateBall(self, x, y):
        self._ballX = x
        self._ballY = y

    def updateWinner(self, playerTwo = False):
        offsetX = 57 if playerTwo else 2
        offsetY = 4 if playerTwo else 1

        for position in self._letters:
            self._board[offsetY + position[1]][offsetX + position[0]] = True
            
        

