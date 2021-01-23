from detailed_code.game import Game
from detailed_code.level import parseLevelTextFile

levels = {
    "tuto": ["tuto1", "tuto2"],
    "test":
        ["easy{}".format(i) for i in range(1, 6)] +
        ["medium{}".format(i) for i in range(1, 5)] +
        ["hard{}".format(i) for i in range(1, 6)]
}


def debug(fileName, stepByStep=True, intraFrame=True):
    test(fileName, True,  stepByStep, intraFrame)


def test(fileName, debug=False, stepByStep=False, intraFrame=False):
    maze_str = parseLevelTextFile(fileName)
    game = Game(maze_str)
    isWon, isDead, isTimeout, score, frame = game.startGame(debug, stepByStep, intraFrame)
    if isWon:
        s = "OK"
    elif isDead:
        s = "KO"
    elif isTimeout:
        s = "Timeout"
    else:
        s = "?"
    print(s, "\t", "Score:", score)

    if not stepByStep and (isDead or isTimeout):
        game.printLevelCamera()
    return isWon, isDead, isTimeout, score, frame


def testAll():
    success = 0
    total = 0

    for folder, files in levels.items():
        for level_file in files:
            total += 1
            fileTested = "{}/{}".format(folder, level_file)
            print("Testing:", fileTested)
            isWon, isDead, isTimeout, score, frame = test(fileTested, False, False, False)
            if isWon:
                success += 1
            print()
