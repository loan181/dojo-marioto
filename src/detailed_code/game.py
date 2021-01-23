from detailed_code.level import Level
from ia import step
from detailed_code.mario import Mario


class Game:
    def __init__(self, level_str):
        self._level = Level(level_str)
        self._player: Mario = self._level.getPlayer()

        self._frame = None
        self._penality = None

    def startGame(self, debug=False, stepByStep=False, intraFrame=False):
        self._frame = 0
        self._penality = 0
        self._player.intraFrame = intraFrame

        MAX_FRAME = 10
        while self._frame <= MAX_FRAME and not self._player.isDead() and not self._player.isWon():
            if debug and stepByStep:
                self.printLevelCamera()
            step(self)  # User defined

            # input("Next?")
            self._frame += 1

        if debug:
            self.printLevelCamera()
        isTimeout = self._frame > MAX_FRAME
        if debug:
            if self._player.isWon():
                print("Gagné!")
            elif self._player.isDead():
                print("GAME OVER!")
            elif isTimeout:
                print("Timeout!")
        score = 0
        if self._player.isWon():
            score = max(0, 5000-self._penality)
            if self._player.getCoin():
                score += 1000
        return self._player.isWon(), self._player.isDead(), isTimeout, score, self._frame

    def printLevelCamera(self):
        print("Frame: {} \t Pénalité de mouvement: {}".format(self._frame, self._penality))
        self._level.printLevelCamera()
        print()

    def playerMoveForward(self):
        self._penality += 20
        self._player.moveForward()

    def playerSprint(self):
        self._penality += 50
        self._player.sprint()

    def playerJump(self):
        self._penality += 80
        self._player.jump()

    def playerHighJump(self):
        self._penality += 100
        self._player.highJump()

    def playerLongJump(self):
        self._player.longJump()
        self._penality += 70

    def playerTurnAround(self):
        self._penality += 10
        self._player.turnAround()

    def getTilesAt(self, camera_x, camera_y):
        self._penality += 1
        return self._level.getCameraTilesAt(camera_x, camera_y)

