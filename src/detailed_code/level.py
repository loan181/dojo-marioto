from detailed_code.tile import TILE
from detailed_code.mario import Mario

def parseLevelTextFile(fileName):
    levelStr = []
    w = -1
    h = 0
    with open("src/level/{}.txt".format(fileName)) as levelTxt:
        for line in levelTxt:
            lenLineStriped = len(line.strip("\n"))
            if w == -1:
                w = lenLineStriped
            elif w != lenLineStriped:
                raise ValueError("Your maze is not rectangular")
            mazeLine = []
            for char in line:
                if char in (".", " "):
                    mazeLine.append(TILE.free)
                elif char == "X":
                    mazeLine.append(TILE.wall)
                elif char == "C":
                    mazeLine.append(TILE.coin)
                elif char == "L":
                    mazeLine.append(TILE.lava)
                elif char == "\n":
                    pass
                else:
                    raise ValueError("Unknown tiles tiles detected: '{}'".format(char))
            levelStr.append(mazeLine)
            h += 1
    # Automatically add the player on the bottom left, goal on bottom right
    levelStr[h - 2][0] = TILE.player
    levelStr[h - 1][0] = TILE.wall
    levelStr[h - 2][w - 1] = TILE.goal
    levelStr[h - 1][w - 1] = TILE.wall
    return levelStr


class Level:
    CAMERA_LEFT = 3
    CAMERA_RIGHT = 6
    CAMERA_DOWN = 2
    CAMERA_UP = 4

    def __init__(self, level):
        self._level = level
        self._player: Mario

        self._initPlayer()

    def _initPlayer(self):
        found = False
        for i in range(len(self._level)):
            line = self._level[i]
            for j in range(len(line)):
                tile = line[j]
                if tile == TILE.player:
                    if found:
                        raise ValueError("Their is more than one player")
                    self._player = Mario(self, j, self._getHeight()-1-i)
                    self._level[i][j] = TILE.free
                    found = True
        if not found:
            raise ValueError("Their is no player")

    def getPlayer(self):
        return self._player

    def _getWidth(self):
        return len(self._level[0])

    def _getHeight(self):
        return len(self._level)

    def getTileAtPosition(self, x, y):
        if y < 0:
            return TILE.lava
        elif x < 0 or x >= self._getWidth():
            return TILE.wall
        elif y >= self._getHeight():
            return TILE.free
        else:
            y_reverse = self._getHeight()-1-y
            return self._level[y_reverse][x]

    def getCameraTilesAt(self, camera_x, camera_y):
        oob = False
        error_message = "Tiles out of camera view for: "
        if camera_x < -Level.CAMERA_LEFT or camera_x > Level.CAMERA_RIGHT:
            oob = True
            error_message += "\n camera_x: {}".format(camera_x)
        if camera_y < -Level.CAMERA_DOWN or camera_y > Level.CAMERA_UP:
            oob = True
            error_message += "\n camera_y: {}".format(camera_y)
        if oob:
            raise ValueError(error_message)

        mario_x = self._player.getX()
        mario_y = self._player.getY()
        return self.getTileAtPosition(mario_x+camera_x, mario_y+camera_y)


    def _setTileAtPosition(self, x, y, tile: TILE):
        y_reverse = self._getHeight() - 1 - y
        self._level[y_reverse][x] = tile

    def isTileAtPositionSolid(self, x, y):
        return self.getTileAtPosition(x, y) == TILE.wall

    def isTileAtPositionKilling(self, x, y):
        return self.getTileAtPosition(x, y) == TILE.lava

    def isTileAtPositionGoal(self, x, y):
        return self.getTileAtPosition(x, y) == TILE.goal

    def isTileAtPositionCoin(self, x, y):
        return self.getTileAtPosition(x, y) == TILE.coin

    def destroyCoinAtPosition(self, x, y):
        if self.isTileAtPositionCoin(x, y):
            self._setTileAtPosition(x, y, TILE.free)

    def printLevelCamera(self):
        mario_x = self._player.getX()
        mario_y = self._player.getY()

        camera_view = []
        for y_offset in range(self.CAMERA_UP, -(self.CAMERA_DOWN+1), -1):
            y_view = mario_y + y_offset
            cur_line = []
            for x_offset in range(-self.CAMERA_LEFT, self.CAMERA_RIGHT+1):
                x_view = mario_x + x_offset
                cur_line.append(self.getTileAtPosition(x_view, y_view))
            camera_view.append(cur_line)

        s = ""
        for y in range(len(camera_view)):
            line = camera_view[y]
            for x in range(len(line)):
                tile = line[x]
                char = str(tile)
                if x == self.CAMERA_LEFT and y == self.CAMERA_UP:
                    char = str(self._player)
                s += char
            s += "\n"
        print(s)


