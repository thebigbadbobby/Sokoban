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
#   Wall  = 0
#   Space = 1
#   Dot   = 2
#   Crate = _0
#   Person= _1

model=encoder((28, 28, 1),4)
# board=[[1, 1, 0, 0, 0, 0, 0, 1],
#        [0, 0, 0, 1, 1, 1, 0, 1],
#        [0, 2,11,10, 1, 1, 0, 1],
#        [0, 0, 0, 1,10, 2, 0, 1],
#        [0, 2, 0, 0,10, 1, 0, 1],
#        [0, 1, 0, 1, 2, 1, 0, 0],
#        [0,10, 1,20,10,10, 2, 0],
#        [0, 1, 1, 1, 2, 1, 1, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0]]

board=[[0, 0, 0, 0],
      [0, 1, 2, 0],
      [0, 1,10, 0],
      [0,11, 1, 0],
      [0, 0, 0, 0]]

print(solve(board, model, 1000))

