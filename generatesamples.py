import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras import layers
from tensorflow import keras
import random
import time
import copy
from inversegame import inversegame
from model import *
#   Wall  = 0
#   Space = 1
#   Dot   = 2
#   Crate = _0
#   Person= _1
model=encoder((28, 28, 1),8)
def place_crates(rows, cols, boxes):
    board=np.random.rand(rows-2,cols-2)
    print(board)
    max_=np.sort(board.flatten())[boxes]
    person=np.sort(board.flatten())[-1]
    for i,row in enumerate(board[0:len(board)]):
        for j,entry in enumerate(row[0:len(row)]):
            if entry<max_:
                board[i][j]=20
            elif entry==person:
                board[i][j]=11
            else:
                board[i][j]=1
    board=np.pad(board, [(1,1),(1,1)])
    return board
def generate_sokoban(model, rows, cols, boxes):
    board=place_crates(rows, cols, boxes)
    generated=inversegame(board)
    # print(generated.board)
    # generated.process("S")
    # print(generated.board)
    index=0
    overallPercentSolved=1
    overallHighestState=inversegame(board)
    criticalstates={copy.deepcopy(generated).toString():copy.deepcopy(generated)}
    while generated.heuristics['percentSolved']!=0:
        oldPercentSolved=generated.heuristics['percentSolved']
        # print(oldPercentSolved)
        print(generated.toString(), index)
        while not generated.heuristics['isLoop']:
            if oldPercentSolved>generated.heuristics['percentSolved']:
                oldPercentSolved=generated.heuristics['percentSolved']
                criticalstates[generated.toString()]=copy.deepcopy(generated)
                if overallPercentSolved>generated.heuristics['percentSolved']:
                    overallPercentSolved=generated.heuristics['percentSolved']
                    overallHighestState=copy.deepcopy(generated)
                break
            # print(example.toString())
            # print(example.commandHistory)
            action=getActionFromArray(arraySum(model.predict(encodeboard(generated.board, 28))))
            generated.process(action)
            index+=1
            if index>200:
                trace(inversegame(board),overallHighestState.commandHistory)
                print(overallHighestState.toString())
                print("koffing", overallPercentSolved)
                print("arbok",overallHighestState.commandHistory)
                return overallHighestState
        # print(example.toString())
        if generated.heuristics['percentSolved']==0:
            break
        generated=copy.deepcopy(random.choice(list(criticalstates.values())))
    trace(inversegame(board),generated.commandHistory)
    print(generated.toString())
    print("koffing")
    print("arbok",generated.commandHistory)
    return generated
    # while True:
    #     action=getActionFromArray(arraySum(model.predict(encodeboard(generated.board, (28,28)))))
    #     if action=="STOP":
    #         break
    #     generated.process(action)
    # return generated
ekans=generate_sokoban(model, 6, 6, 3)
# while ekans.isWon():
#     ekans=generate_sokoban(model, 6, 6, 3)
# print(ekans.board)