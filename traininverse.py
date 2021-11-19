from generatesamples import generate_sokoban as generate
from solvesamples import solve_sokoban as solve
from model import *
def evaluateperformance(samples, model, invmodel, maxiter):
    results=[]
    for i in range(0,samples):
        board=generate(invmodel, 5,5,2).board
        results.append(solve(board, model, maxiter))
    print(results)
model=encoder((28, 28, 1),4)
invmodel=encoder((28, 28, 1),8)
evaluateperformance(10, model, invmodel, 100)