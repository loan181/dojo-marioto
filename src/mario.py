
class DIRECTION:
    right = "→"
    up = "↑"
    left = "←"
    down = "↓"

    _dirs = (right, up, left, down)

    def __init__(self, dir):
        self._dir = dir

    def _getIndexInDir(self):
        return self._dirs.index(self._dir)

    def rotateLeft(self):
        ind = self._getIndexInDir()
        self._dir = self._dirs[(ind + 1) % len(self._dirs)]

    def rotateRight(self):
        ind = self._getIndexInDir()
        self._dir = self._dirs[(ind - 1) % len(self._dirs)]

    def getForwardPosition(self, x, y):
        if self._dir == DIRECTION.right:
            return x + 1, y
        elif self._dir == DIRECTION.up:
            return x, y + 1
        elif self._dir == DIRECTION.left:
            return x - 1, y
        elif self._dir == DIRECTION.down:
            return x, y - 1

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self._dir


class Mario:
    def __init__(self, level, x, y):
        self._level = level
        self._x = x
        self._y = y

        self._dead = False
        self._won = False
        self._coin = False
        self._direction: DIRECTION = DIRECTION(DIRECTION.right)

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getDirection(self):
        return self._direction
    
    def isDead(self):
        return self._dead

    def isWon(self):
        return self._won

    def getCoin(self):
        return self._coin

    # Actions #
    def _applyMovesIfPossible(self, moves):
        if self._dead:
            return

        canMove = True
        indMove = 0
        direction = None
        while canMove and not self._dead and indMove < len(moves):
            direction = moves[indMove]
            next_x, next_y = direction.getForwardPosition(self._x, self._y)
            if not self._level.isTileAtPositionSolid(next_x, next_y):
                self._x = next_x
                self._y = next_y
                self._checkIfCoin()
                self._checkIfWon()
                self._checkIfDead()
            else:
                # Note that the move could be partially applied, this is intentional
                canMove = False

            indMove += 1
        if direction != DIRECTION(DIRECTION.down) or canMove:
            self.applyGravity()

    def moveForward(self):
        self._applyMovesIfPossible([self._direction])

    def jump(self):
        self._applyMovesIfPossible([
            DIRECTION(DIRECTION.up),
            self._direction,
            DIRECTION(DIRECTION.up),
            self._direction
        ])

    def highJump(self):
        self._applyMovesIfPossible([
            DIRECTION(DIRECTION.up),
            DIRECTION(DIRECTION.up),
            DIRECTION(DIRECTION.up),
            self._direction
        ])

    def longJump(self):
        self._applyMovesIfPossible([
            self._direction,
            DIRECTION(DIRECTION.up),
            self._direction,
            self._direction,
        ])

    def sprint(self):
        self._applyMovesIfPossible([
            self._direction,
            self._direction
        ])

    def turnAround(self):
        if self._direction == DIRECTION(DIRECTION.right):
            self._direction = DIRECTION(DIRECTION.left)
        else:
            self._direction = DIRECTION(DIRECTION.right)

    # Other #
    def applyGravity(self):
        self._applyMovesIfPossible([DIRECTION(DIRECTION.down)])

    def _checkIfDead(self):
        if not self._dead:
            self._dead = self._level.isTileAtPositionKilling(self._x, self._y)

    def _checkIfWon(self):
        if not self._won:
            self._won = self._level.isTileAtPositionGoal(self._x, self._y)

    def _checkIfCoin(self):
        if not self._coin:
            if self._level.isTileAtPositionCoin(self._x, self._y):
                self._coin = True
                self._level.destroyCoinAtPosition(self._x, self._y)

    def __str__(self):
        return str(self._direction)
