from model import *
from game import game
def solve_sokoban(board, model, maxiter):
    index=0
    example=game(board)
    criticalstates={copy.deepcopy(example).toString():copy.deepcopy(example)}
    while example.heuristics['percentSolved']!=1:
        oldPercentSolved=example.heuristics['percentSolved']
        # print(oldPercentSolved)
        print(example.toString(), index)
        while not example.heuristics['isLoop']:
            if oldPercentSolved<example.heuristics['percentSolved']:
                oldPercentSolved=example.heuristics['percentSolved']
                criticalstates[example.toString()]=copy.deepcopy(example)
                break
            # print(example.toString())
            # print(example.commandHistory)
            action=getActionFromArray(arraySum(model.predict(encodeboard(example.board, (28,28)))))
            example.process(action)
            # print(example.toString(), index)
            index+=1
            if index>maxiter:
                return -1
        # print(example.toString())
        if example.heuristics['percentSolved']==1:
            break
        example=copy.deepcopy(random.choice(list(criticalstates.values())))
    print("weezing",trace(game(board),example.commandHistory))
    print(example.toString())
    print(example.commandHistory)
    return index