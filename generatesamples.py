import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras import layers
from tensorflow import keras
import random
import time
import copy
from inversegame import inversegame
from game import game
from model import *
#   Wall  = 0
#   Space = 1
#   Dot   = 2
#   Crate = _0
#   Person= _1
model=encoder((28, 28, 1),8)
def add_walls(board, walllist):
    if len(board)==0:
        return board
    for wall in walllist:
        randnum=random.uniform(0,1)
        if randnum<.5:
            board[:,int(wall.replace("[","").replace("]","").replace(",","").split()[0]),int(wall.replace("[","").replace("]","").replace(",","").split()[1])]=0
    return board
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
def generate_sokoban(model, rows, cols, boxes, ):
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
        print(overallHighestState.toString(), index)
        while not generated.heuristics['isLoop']:
            if oldPercentSolved>generated.heuristics['percentSolved']:
                oldPercentSolved=generated.heuristics['percentSolved']
                criticalstates[generated.toString()]=copy.deepcopy(generated)
                if overallPercentSolved>generated.heuristics['percentSolved']:
                    overallPercentSolved=generated.heuristics['percentSolved']
                    overallHighestState=copy.deepcopy(criticalstates[generated.toString()])
                    print("stamped", overallHighestState.toString())
                break
            # print(example.toString())
            # print(example.commandHistory)
            action=getActionFromArray(arraySum(model.predict(encodeboard(generated.board, (28,28)))))
            generated.process(action)
            print("geodude")
            index+=1
            if index>170:
                return overallHighestState
        # print(example.toString())
        if generated.heuristics['percentSolved']==0:
            break
        generated=copy.deepcopy(random.choice(list(criticalstates.values())))
    
    return generated
    # while True:
    #     action=getActionFromArray(arraySum(model.predict(encodeboard(generated.board, (28,28)))))
    #     if action=="STOP":
    #         break
    #     generated.process(action)
    # return generated

    # def trainingpak():
    #     ekans=
generated=generate_sokoban(model, 6, 6, 3)
traces=trace(game(generated.board[:]),generated.commandHistory)
for i in range(0, 5):
    print("weezing", add_walls(traces[2],traces[0]))

# print(generated.toString())
# print("koffing")
# print("arbok",traces[1])
# print(traces[2])
    
# print()
# while ekans.isWon():
#     ekans=generate_sokoban(model, 6, 6, 3)
# print(ekans.board)