import numpy as np
import random
import time
import copy
from model import *
from game import game
from solvesamples import solve_sokoban as solve
import sys, getopt
import datetime
from Play import play

import torch

from game import game
from Network.torchBasic import torchBasic
from trainer import Trainer
import os
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#   Wall  = 0
#   Space = 1
#   Dot   = 2
#   Crate = _0
#   Person= _1
size = 45
maxrow = 45
maxcol = 35
maxsize = maxrow * maxcol
# model=encoder((size, size, 1),4)


argsLearn = {
    'batch_size': 5,
    'numIters': 100,                                # Total number of training iterations
    'num_simulations': 20,                         # Total number of MCTS simulations to run when deciding on a move to play
    'numEps': 10,                                  # Number of full games (episodes) to run during each iteration
    'epochs': 20,                                    # Number of epochs of training per iteration
    'checkpoint_path': 'latest.pth',                 # location to save latest set of weights
    'loopStop': 10                                   #stop it from going into infinite loops
}


def main(args):
      path = './error/'
      if not os.path.exists(path):
            os.makedirs(path)
      path = './models/'
      if not os.path.exists(path):
            os.makedirs(path)
      row, col = 0, 0
      numWall = 0
      wallCords = []
      noStorage = 0
      storCords = []
      noBox = 0
      boxCords = []
      playerStart = (0, 0)
      count = 0
      f = open(args[0], 'r')
      row, col = [int(x) for x in next(f).split()]
      for line in f:
            lineSplit = line.split()
            if count == 0:
                  numWall = int(lineSplit.pop(0))
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
      board = np.zeros((row, col))
      board[playerStart[0] - 1][playerStart[1] - 1] = 11
      for (x, y) in boxCords:
            board[x-1][y-1] = 10
      for (x, y) in storCords:
            board[x-1][y-1] = 2
            
      for i in range(0, row):
            for j in range(0, col):
                  if (i, j) not in wallCords and board[i][j] ==0:
                        board[i][j] = 1

      row = board.shape[0]
      col = board.shape[1]
      board = encodeboard(board, (maxrow, maxcol))
      sokoban = game(board, row, col, maxrow, maxcol)
      board_size = maxsize
      action_size = maxsize
      model = torchBasic(board_size, action_size, device)
      if len(args) > 1:
            model.load_state_dict(torch.load(args[1]))
            # argsLearn['checkpoint_path'] = args[1]
      if len(args) < 3:
            x = str(datetime.datetime.now())
            fname = './error/error-' + x + '.csv'
            fp = open(fname, 'x')
            fp.close()
            trainer = Trainer(board, model, argsLearn, maxsize, row, col, maxrow, maxcol, fname)
            trainer.learn()
      else:
            print('play')
            newgame = play(board, model, argsLearn, maxsize, row, col, maxrow, maxcol)
            newgame.playGame()
      


if __name__ == "__main__":
      main(sys.argv[1:])
