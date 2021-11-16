from inversegame import inversegame as game
from generatesamples import generate_sokoban as generate
def getnextmove(game):
        keypress=input("which way "+str(game.commandLookup.keys())+"?")
        return keypress
board=generate(7,7,3).board
example=game(board)
while True:
    action=getnextmove(example)
    example.process(action)
    # trace(game(board),example.commandHistory)
    print(example.toString())
    print(example.commandHistory)
