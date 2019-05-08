import random
import Draw
import Constants
import Timing
import JoystickController
import Glow


class Ball:
    position = [3, Constants.height // 2]
    direction_x = 1
    direction_y = 0

    speed = Constants.speed[0]
    time_to_next_move = 0.0

    def __init__(self):
        # Reset speed and direction
        self.set_position()
        self.set_direction()

    def set_speed(self, speed):
        self.speed = speed

    def set_position(self, position = [3, Constants.height // 2]):
        self.position = [position[0], position[1]]

    def set_direction(self, direction = [1, 0]):
        self.direction_x = direction[0]
        self.direction_y = direction[1]


    def move(self, delta_time):
        self.time_to_next_move -= delta_time
        # If it's time for the ball to move
        if self.time_to_next_move <= 0:
            # Update the ball's position according to its direction
            self.position[0] += self.direction_x
            self.position[0] += self.direction_y
            self.time_to_next_move = self.speed


class Bat:
    position = Constants.height // 2
    score = 0

    is_big = False
    can_big = True
    big_time = 2000

    def __init__(self, position: int = None):
        if position is not None:
            self.position = position

    def update(self, delta_time, movement):
        self.big_time -= delta_time
        if self.big_time <= 0 and self.is_big:
            self.is_big = False
        self.move(movement)

    def set_position(self, *position):
        # If a position is given, set it to that
        if position is not None:
            self.position = position
        # If there's no position, assume it's being reset
        else:
            self.position = Constants.height // 2

    # We wanna make sure our midpoint doesn't mean we're outside our game.
    # So anything below 2 becomes 2, anything above 22 becomes 22. If big bats then 3 < x < 24
    # bats are 1x3 despite image making them look 1x4. Regardless,
    # this makes things easier. Take pos to be the midpoint.
    def move(self, movement):
        self.position += movement

        if self.position < (3 if self.is_big else 2):
            self.position = (3 if self.is_big else 2)
        elif self.position > (20 if self.is_big else 22):
            self.position = (20 if self.is_big else 22)

    def make_big(self):
        if self.can_big:
            self.is_big = True
            self.can_big = False

    def check_hit(self, ball_y):
        if self.is_big:
            if -1 <= (self.position - ball_y) <= 1:
                return True
        else:
            if -2 <= (self.position - ball_y) <= 3:
                return True
        return False


class Pong:

    # Utility classes
    timer = Timing.Timing()
    board = Draw.Board(Constants.length, Constants.height)

    # Gameplay classes
    player_one = Bat()
    player_two = Bat()
    ball = Ball()

    player_one_controller = JoystickController.JoystickController()

    # Game state vars
    serving = True
    playerTwoIsServing = False
    serves = 0
    gameOver = False

    def start(self):
        # Setup the board by putting the bats and ball in the right place
        self.board.updateBats(self.player_one.position, self.player_two.position,
                              self.player_one.is_big, self.player_two.is_big)

        self.board.updateBall(self.ball.position[0], self.ball.position[1])

        # Run the game loop until the game is over
        while not self.gameOver:
            self.game_loop()

    def game_loop(self):
        # Get the last frame time
        self.timer.update_time()

        # Simulate random presses of the 'make big' button
        if random.randint(0, 250) == 9:
            self.player_one.make_big()
        if random.randint(0, 250) == 9:
            self.player_two.make_big()

        # Update the status of the joystick controllers
        self.player_one_controller.update()

        # Emulate random bat movement and update the big_time on the Bat
        #self.player_one.update(self.timer.deltaTime, random.randint(-1, 1))
        self.player_one.update(self.timer.deltaTime, self.player_one_controller.get_delta_resistor_position())
        self.player_two.update(self.timer.deltaTime, random.randint(-1, 1))

        # If the current game state is serving, set up a serve
        if self.serving:
            self.setup_serve()

            # Emulate a serve
            if random.randint(0, 100) == 9:
                if not self.playerTwoIsServing:
                    self.ball.set_direction(1, random.randrange(-1, 1, 2))
                else:
                    self.ball.set_direction(-1, random.randrange(-1, 1, 2))

                # Change the game state and the next serve
                self.serving = False
                self.serves += 1
                if self.serves == 5:
                    self.playerTwoIsServing = not self.playerTwoIsServing

        # If the current game state is not serving (ie. playing)
        else:
            # Move the ball
            self.ball.move(self.timer.deltaTime)
            if self.ball.position[1] == 0 or self.ball.position[0] == Constants.height - 1:
                self.ball.direction_y *= -1

            if self.ball.position[0] == 2 or self.ball.position[0] == Constants.length - 3:
                print("Ball may have hit bat")

                if self.player_one.check_hit(self.ball.position[1]):
                    print("Player one has hit the ball")
                    self.reverse_ball_direction()
                elif self.player_two.check_hit(self.ball.position[1]):
                    print("Player two has hit the ball")
                    self.reverse_ball_direction()

        # Write the current game state to the board
        self.board.prepare()
        self.board.updateBats(self.player_one.position, self.player_two.position,
                              self.player_one.is_big, self.player_two.is_big)

        self.board.updateBall(self.ball.position[0], self.ball.position[1])

        # If a player has scored, update their score and change the state to serving
        if self.ball.position[0] == 0:
            self.player_one.score += 1
            Glow.score()
            self.set_serving()
            self.board.updateScore(self.player_one.score)
        elif self.ball.position[0] == Constants.length - 1:
            self.player_two.score += 1
            Glow.score()
            self.set_serving()
            self.board.updateScore(self.player_two.score, True)

        # Check if either player has won the game
        self.check_winner()

        # Draw the board and wait until it needs to be drawn again
        self.board.draw()
        self.timer.wait_for_update()

    def set_serving(self):
        self.serving = True
        self.player_one.set_position(None)
        self.player_two.set_position(None)

    def setup_serve(self):
        if not self.playerTwoIsServing:
            self.ball.set_position([3, self.player_one.position])
        else:
            self.ball.set_position([Constants.length - 4, self.player_two.position])

    def reverse_ball_direction(self):
        self.ball.direction_y *= 1
        self.ball.direction_x *= -1
        self.ball.set_speed(random.choice(Constants.speed))

    def check_winner(self):
        # If either player has a score greater than 9, they win
        if self.player_one.score > 9:
            self.gameOver = True
            return True
        elif self.player_two.score > 9:
            self.gameOver = True
            return True
        return False
