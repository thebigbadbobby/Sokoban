import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras import layers
from tensorflow import keras
import random
import time
import copy
OPPOSITES={"leftPull":"right", "left": "right", "rightPull":"left", "right":"left", "upPull":"down", "up":"down", "downPull": "up", "down":"up"}
def encodeboard(board, size):
    bigboard=np.zeros(size)
    bigboard[:np.array(board).shape[0],:np.array(board).shape[1]]=np.array(board)
    
    return bigboard
def arraySum(array):
    sums=0
    for i in range(0,len(array[0])):
        sums+=abs(array[0][i])
        array[0][i]=sums
    array[0]/=sums
    # print("ekans", array[0])
    return array[0]
# array=[.25,.25,.25,.25]
# arraySum(array)
def getActionFromArray(array):
    randnum=random.uniform(0,1)
    if randnum < array[0]:
        return "a"
    if randnum < array[1]:
        return "w"
    if randnum < array[2]:
        return "s"
    if randnum < array[3]:
        return "d"
    if randnum < array[4]:
        return "A"
    if randnum < array[5]:
        return "W"
    if randnum < array[6]:
        return "S"
    if randnum < array[7]:
        return "D"
    return "STOP"
def trace(game, commandHistory):
    personset=set()
    clearset=game.clearSet()
    boardarray=[]
    for command in commandHistory[::-1]:
        if command!='start' and game.isWon()!=True:
            print(game.toString())
            a=copy.deepcopy(game.board)
            boardarray.append(a)
            game.process(OPPOSITES[command])
            personset={str(game.findPerson())}|personset
    if not game.isWon():
        ekans={}
        print(np.array(boardarray),clearset.difference(personset|{""}))
        print(ekans[0])
    return [clearset.difference(personset|{""}), game.commandHistory[1:], np.array(boardarray)]
def encoder(input_encoder,size):
    
    inputs = keras.Input(shape=input_encoder, name='input_layer')
    x = layers.Conv2D(32, kernel_size=3, strides= 1, padding='same', name='conv_1')(inputs)
    x = layers.BatchNormalization(name='bn_1')(x)
    x = layers.LeakyReLU(name='lrelu_1')(x)
    
    
    x = layers.Conv2D(64, kernel_size=3, strides= 2, padding='same', name='conv_2')(x)
    x = layers.BatchNormalization(name='bn_2')(x)
    x = layers.LeakyReLU(name='lrelu_2')(x)
    
    
    x = layers.Conv2D(64, 3, 2, padding='same', name='conv_3')(x)
    x = layers.BatchNormalization(name='bn_3')(x)
    x = layers.LeakyReLU(name='lrelu_3')(x)
  

    x = layers.Conv2D(64, 3, 1, padding='same', name='conv_4')(x)
    x = layers.BatchNormalization(name='bn_4')(x)
    x = layers.LeakyReLU(name='lrelu_4')(x)
   
    
    flatten = layers.Flatten()(x)
    mean = layers.Dense(size, name='mean')(flatten)
    model = tf.keras.Model(inputs, (mean), name="Encoder")
    return model