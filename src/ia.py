
def step(game):
    # Si c'est libre devant (ou l'objectif) et qu'il y a du sol en dessous
    if game.getTilesAt(1, 0) in (" ", "G") and game.getTilesAt(1, -1) == "X":
        game.playerMoveForward()
    # S'il y a un trou suivi d'un bloc
    elif game.getTilesAt(1, 0) == " " and game.getTilesAt(1, -1) == " " and game.getTilesAt(2, -1) == "X":
        game.playerJump()
    else:
        game.playerLongJump()