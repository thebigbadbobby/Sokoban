import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras import layers
from tensorflow import keras
import random
import time
import copy
from model import *
from game import game
from solvesamples import solve_sokoban as solve
import sys, getopt
#   Wall  = 0
#   Space = 1
#   Dot   = 2
#   Crate = _0
#   Person= _1
size = 28
model=encoder((size, size, 1),4)
# board=[[1, 1, 0, 0, 0, 0, 0, 1],
#        [0, 0, 0, 1, 1, 1, 0, 1],
#        [0, 2,11,10, 1, 1, 0, 1],
#        [0, 0, 0, 1,10, 2, 0, 1],
#        [0, 2, 0, 0,10, 1, 0, 1],
#        [0, 1, 0, 1, 2, 1, 0, 0],
#        [0,10, 1,20,10,10, 2, 0],
#        [0, 1, 1, 1, 2, 1, 1, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0]]

# board=[[0, 0, 0, 0],
#       [0, 1, 2, 0],
#       [0, 1,10, 0],
#       [0,11, 1, 0],
#       [0, 0, 0, 0]]

# print(solve(board, model, 1000))


def main(args):
      row, col = 0, 0
      numWall = 0
      wallCords = []
      noStorage = 0
      storCords = []
      noBox = 0
      boxCords = []
      playerStart = (0, 0)
      count = 0
      print(args)
      f = open(args[0], 'r')
      row, col = [int(x) for x in next(f).split()]
      for line in f:
            lineSplit = line.split()
            if count == 0:
                  numWall = int(lineSplit.pop(0))
                  print(lineSplit)
                  print(len(lineSplit))
                  for i in range(0, len(lineSplit), 2):
                        wallCords.append((int(lineSplit[i]) - 1, (int(lineSplit[i+1])) - 1))
                  
            if count == 1:
                  noBox = int(lineSplit.pop(0))
                  for i in range(0, len(lineSplit), 2):
                        boxCords.append((int(lineSplit[i]), (int(lineSplit[i+1]))))
            if count == 2:
                  noStorage = int(lineSplit.pop(0))
                  for i in range(0, len(lineSplit), 2):
                        storCords.append((int(lineSplit[i]), (int(lineSplit[i+1]))))
            if count == 3:
                  playerStart = (int(lineSplit[0]), int(lineSplit[1]))
            count += 1
      f.close()
      # print(numWall)
      # print(noStorage)
      # print(noBox)
      # print(playerStart)
      # print(wallCords)
      # print(boxCords)
      # print(storCords)
      board = np.zeros((row, col))
      # print(board)
      board[playerStart[0] - 1][playerStart[1] - 1] = 11
      for (x, y) in boxCords:
            board[x-1][y-1] = 10
      for (x, y) in storCords:
            board[x-1][y-1] = 2
      for i in range(0, row):
            for j in range(0, col):
                  if (i, j) not in wallCords and board[i][j] ==0:
                        board[i][j] = 1
      print(board)
      # print(game(board).toString())
      # print(board)
      print(solve(board, model, 3))
      
      


if __name__ == "__main__":
      main(sys.argv[1:])
