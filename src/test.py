from game import Game
from level import parseLevelTextFile

levels = {
    "tuto": ["tuto1", "tuto2"],
    "test":
        ["easy{}".format(i) for i in range(1, 6)] +
        ["medium{}".format(i) for i in range(1, 5)]
}


def debug(fileName, stepByStep=False):
    maze_str = parseLevelTextFile(fileName)
    game = Game(maze_str)
    game.startGame(True, stepByStep)


def testAll():
    success = 0
    total = 0

    for folder, files in levels.items():
        for level_file in files:
            total += 1
            fileTested = "{}/{}".format(folder, level_file)
            print("Testing:", fileTested)
            level_str = parseLevelTextFile(fileTested)
            game = Game(level_str)
            isWon, isDead, isTimeout, score, frame = game.startGame()
            if isWon:
                success += 1
                s = "OK"
            elif isDead:
                s = "KO"
            elif isTimeout:
                s = "Timeout"
            else:
                s = "?"
            print("\t", s, "Score:", score)

            if isDead or isTimeout:
                game.printLevelCamera()
            print()