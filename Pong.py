import random
import Draw
import Constants
import Timing
import JoystickController
import Glow
import Sound

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

    def set_position(self, position=None):
        if position is None:
            position = [3, Constants.height // 2]
        self.position = [position[0], position[1]]

    def set_direction(self, direction=None):
        if direction is None:
            direction = [1, 0]
        self.direction_x = direction[0]
        self.direction_y = direction[1]

    def move(self):
        # If it's time for the ball to move
        if self.time_to_next_move <= 0:
            # Update the ball's position according to its direction
            self.position[0] += self.direction_x
            self.position[1] += self.direction_y
            self.time_to_next_move = self.speed

    def update(self, delta_time):
        self.time_to_next_move -= delta_time
        self.move()


class Bat:
    position = Constants.height // 2
    score = 0

    is_big = False
    can_big = 2
    big_time = Constants.big_time

    def __init__(self, position=None):
        if position is not None:

            self.position = position

    def update(self, delta_time, position):
        if self.is_big:
            self.big_time -= delta_time
            if self.big_time <= 0:
                self.is_big = False
        self.set_position(position)

    def set_position(self, position=None):
        if position is None:
            position = Constants.height // 2
        if self.is_big:
            if 2 <= position < 20:
                self.position = position
        else:
            if 0 <= position < 22:
                self.position = position

    # We wanna make sure our midpoint doesn't mean we're outside our game.
    # So anything below 2 becomes 2, anything above 22 becomes 22. If big bats then 3 < x < 24
    # bats are 1x3 despite image making them look 1x4. Regardless,
    # this makes things easier. Take pos to be the midpoint.
    def move(self, movement):
        self.position += movement

        if self.position < (4 if self.is_big else 2):
            self.position = (4 if self.is_big else 2)
        elif self.position > (18 if self.is_big else 22):
            self.position = (18 if self.is_big else 22)

    def make_big(self):
        if self.can_big > 0:
            if not self.is_big:
                self.big_time = Constants.big_time
                self.is_big = True
                self.can_big -= 1

    def check_hit(self, ball_y):
        if not self.is_big:
            if -1 <= (self.position - ball_y) <= 1:
                return self.position - ball_y
        else:
            if -2 <= (self.position - ball_y) <= 3:
                return self.position - ball_y
        return False


class Pong:
    # Utility classes
    timer = Timing.Timing()
    board = Draw.Board(Constants.length, Constants.height)

    # Gameplay classes
    player_one = Bat()
    player_two = Bat()
    ball = Ball()

    player_one_controller = JoystickController.JoystickController(0x10, 10, 9, True, True)
    player_two_controller = JoystickController.JoystickController(0x20, 0x00, 0x00, True, True)

    # Game state vars
    serving = True
    playerTwoIsServing = False
    serves = 0
    gameOver = False

    def start(self):
        # Let's hope this works...
        Sound.play_async(Sound.start_music)

        self.board.prepare()
        # Setup the board by putting the bats and ball in the right place
        self.board.updateBats(self.player_one.position, self.player_two.position,
                              self.player_one.is_big, self.player_two.is_big)
        self.board.updateBall(self.ball.position[0], self.ball.position[1])
        self.board.updateScore(0, False)
        self.board.updateScore(0, True)

        # Run the game loop until the game is over
        while not self.gameOver:
            self.game_loop()

    def game_loop(self):
        # Get the last frame time
        self.timer.update_time()

        # Update the status of the joystick controllers
        self.player_one_controller.update()
        self.player_two_controller.update()

        # Emulate random bat movement and update the big_time on the Bat
        self.player_one.update(self.timer.deltaTime, self.player_one_controller.get_resistor_screen_position() + 1)
        if self.ball.direction_x == 1:  # If the ball is coming towards the AI
            ai_pos_delta = (self.ball.position[1] - self.player_two.position)
        else:
            ai_pos_delta = (Constants.height // 2 - self.player_two.position)
        if ai_pos_delta != 0:   # If we're not /ing by 0
            if random.randint(0, 1) == 1:   # 50/50 chance to move
                self.player_two.update(self.timer.deltaTime, self.player_two.position + int(abs(ai_pos_delta) / ai_pos_delta))

        # If the current game state is serving, set up a serve
        if self.serving:
            self.setup_serve()

            # Emulate a serve
            if not self.playerTwoIsServing:
                if self.player_one_controller.button_1_pressed == 0:
                    self.ball.set_direction([1, random.randrange(-1, 1)])
                    self.serving = False
                    self.serves += 1
                    if self.serves % 5 == 0:
                        self.playerTwoIsServing = not self.playerTwoIsServing
            else:
                if random.randrange(1, 100) == 9:
                    self.ball.set_direction([-1, random.randrange(-1, 1)])
                    self.serving = False
                    self.serves += 1
                    if self.serves % 5 == 0:
                        self.playerTwoIsServing = not self.playerTwoIsServing

        # If the current game state is not serving (ie. playing)
        else:
            # Move the ball
            self.ball.update(self.timer.deltaTime)

            if self.ball.position[1] == 0:
                self.ball.direction_y *= -1
                self.ball.set_position([self.ball.position[0], self.ball.position[1] + 1])
            elif self.ball.position[1] == Constants.height - 1:
                self.ball.direction_y *= -1
                self.ball.set_position([self.ball.position[0], self.ball.position[1] - 1])

            if self.ball.position[0] == 2 or self.ball.position[0] == 1:
                deltaOne = self.player_one.check_hit(self.ball.position[1])
                if deltaOne:
                    self.reverse_ball_direction(deltaOne)
                    Sound.play_async(Sound.hit_sequence)

            elif self.ball.position[0] == Constants.length - 3 or self.ball.position[0] == Constants.length - 2:
                deltaTwo = self.player_two.check_hit(self.ball.position[1])
                if deltaTwo:
                    self.reverse_ball_direction(deltaTwo)
                    Sound.play_async(Sound.hit_sequence)

            # Check if the player wants to be big
            if self.player_one_controller.button_2_pressed == 0:
                self.player_one.make_big()
            if self.player_two_controller.button_2_pressed == 0:
                self.player_two.make_big()

        # Write the current game state to the board
        self.board.prepare()
        self.board.updateBats(self.player_one.position, self.player_two.position,
                              self.player_one.is_big, self.player_two.is_big)

        self.board.updateBall(self.ball.position[0], self.ball.position[1])
        self.board.updateScore(self.player_one.score)
        self.board.updateScore(self.player_two.score, True)

        # If a player has scored, update their score and change the state to serving
        if self.ball.position[0] == 0:
            self.player_two.score += 1
            Glow.score()
            self.set_serving()
        elif self.ball.position[0] == Constants.length - 1:
            self.player_one.score += 1
            Glow.score()
            self.set_serving()

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

    def reverse_ball_direction(self, delta = 0):
        if delta < 0:
            self.ball.direction_y = -1
        elif delta > 0:
            self.ball.direction_y = 1
        else:
            self.ball.direction_y = 0
            
        self.ball.direction_y = random.randrange(-1, 1)
        self.ball.direction_x *= -1
        self.ball.set_speed(random.choice(Constants.speed))

        Sound.hit()

    def check_winner(self):
        # If either player has a score greater than 9, they win
        if self.player_one.score > 9:
            self.board.updateWinner(False)
            self.gameOver = True
            return True
        elif self.player_two.score > 9:
            self.board.updateWinner(True)
            self.gameOver = True
            return True
        return False