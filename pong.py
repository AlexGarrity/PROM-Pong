from datetime import datetime

import random
import draw, constants
import time

import timing

timer = timing.Timing()

board = draw.Board(constants.length, constants.height)
board.prepare()
# bus.write_line(board.draw())

gametime = float(time.time())
balltime = gametime
updateTime = 1
timeToNextUpdate = 0
serving = False
serves = 0
playerTwoIsServing = False
playerOneBig = True
playerTwoBig = True
playerOneCanBig = True
playerTwoCanBig = True
gameOver = False
speed = constants.speed[0]

# currentNum = 0

# Bat and ball default positions
playerOnePos = constants.height // 2
playerTwoPos = constants.height // 2
playerOneScore = 0
playerTwoScore = 0
ballPos = [3, constants.height // 2]

# ballMovement
ballDirectionX = 1
ballDirectionY = 0

board.updateScore(0)
board.updateScore(0, True)
board.updateBats(playerOnePos, playerTwoPos, playerOneBig, playerTwoBig)
board.updateBall(ballPos[0], ballPos[1])
# Infinite loop, maybe? Probably just stop it if a score reaches 10
# Remember, game logic is stored in this file. So we have the REAL pos of the bats/ball here.
while True:
    # Our game clock. Our tickrate is around 13.3, meaning we update our game that many times per sec.
    currentTime = float(time.time())
    timer.update_time()

    # Checking if we should tick
    if currentTime - gametime >= 1 / constants.tickrate:

        # The process is update game time, update bats (size first, THEN movement),
        # update ball, check if ball is at edge.
        # If yes, update score, if we won then yay. Otherwise reset positions, push "game time"
        # forwards by 2 secs to freeze game. THEN we do serve logic until served
        # regardless: clear board, initialise board, draw scores, draw bats, draw ball.
        gametime = currentTime
        # currentNum = (currentNum + 1) % 10
        # bus.write_line(currentNum)
        # board.updateScore(currentNum)

        # Emulating random button press for big bat
        if random.randint(0, 250) == 9:
            if playerOneBig or playerOneCanBig:
                playerOneBig = not playerOneBig
                playerOneCanBig = False
        if random.randint(0, 250) == 9:
            if playerTwoBig or playerTwoCanBig:
                playerTwoBig = not playerTwoBig
                playerTwoCanBig = False

        # Emulating random bat movement.
        playerOneMove = random.randint(-1, 1)
        playerTwoMove = random.randint(-1, 1)

        playerOnePos += playerOneMove
        playerTwoPos += playerTwoMove

        # We wanna make sure our midpoint doesn't mean we're outside our game.
        # So anything below 2 becomes 2, anything above 22 becomes 22. If big bats then 3 < x < 24
        # bats are 1x3 despite image making them look 1x4. Regardless,
        # this makes things easier. Take pos to be the midpoint.
        if playerOnePos < (3 if playerOneBig else 2):
            playerOnePos = (3 if playerOneBig else 2)
        elif playerOnePos > (20 if playerOneBig else 22):
            playerOnePos = (20 if playerOneBig else 22)
        if playerTwoPos < (3 if playerTwoBig else 2):
            playerTwoPos = (3 if playerTwoBig else 2)
        elif playerTwoPos > (20 if playerTwoBig else 22):
            playerTwoPos = (20 if playerTwoBig else 22)

        if serving:
            ballPos = [constants.length - 4, playerTwoPos] if playerTwoIsServing else [3, playerOnePos]

            # emulating random serve
            if random.randrange(0, 100) == 9:
                ballDirectionY = random.randrange(-1, 1, 2)
                ballDirectionX = -1 if playerTwoIsServing else 1
                serving = False
                serves += 1
                if serves == 5:
                    serves = 0
                    playerTwoIsServing = not playerTwoIsServing

        else:
            # Move our ball.
            if currentTime - balltime >= speed:
                balltime = currentTime
                ballPos = [ballPos[0] + ballDirectionX, ballPos[1] + ballDirectionY]

                # check if we hit the top or bottom, reverse ballDirY
                if ballPos[1] == 0 or ballPos[1] == constants.height - 1:
                    ballDirectionY *= -1

                # check if ball has hit bat, so calc next speed/direction
                if ballPos[0] == 2 or ballPos[0] == constants.length - 3:
                    print("true")
                    # nested if looks nicer
                    # Can confirm
                    if (-2 if playerOneBig else -1) <= playerOnePos - ballPos[1] <= (3 if playerOneBig else 1):
                        print("hit right bat")
                        # set our direction depending whether we hit top, middle, bottom (random right now)
                        ballDirectionY = 1
                        ballDirectionX *= -1
                        speed = random.choice(constants.speed)

                    elif (-2 if playerTwoBig else -1) <= playerTwoPos - ballPos[1] <= (3 if playerTwoBig else 1):
                        print("hit left bat")

                        ballDirectionY = -1
                        ballDirectionX *= -1
                        speed = random.choice(constants.speed)

        board.prepare()
        board.updateBats(playerOnePos, playerTwoPos, playerOneBig, playerTwoBig)
        board.updateBall(ballPos[0], ballPos[1])
        # check if ball is at left/right edge, increase score, next serve.
        if ballPos[0] == 0:
            playerTwoScore += 1
            serving = True
            playerOnePos = constants.height // 2
            playerTwoPos = constants.height // 2
        elif ballPos[0] == constants.length - 1:
            playerOneScore += 1
            serving = True
            playerOnePos = constants.height // 2
            playerTwoPos = constants.height // 2
        board.updateScore(playerOneScore)
        board.updateScore(playerTwoScore, True)
        # check if score is more than 9, win game.
        if playerOneScore > 9:
            board.updateWinner()
            gameOver = True
        elif playerTwoScore > 9:
            gameOver = True
            board.updateWinner(True)
            # os.system("cls")
        board.draw()
        timeToNextUpdate = updateTime - (currentTime - gametime)
        timer.wait_for_update()
        if gameOver:
            break
