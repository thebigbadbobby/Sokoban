# class strategy:
#     def __init__(self, strategyname):
#         self.strategyMethod=getattr(self, strategyname)
#     def apply(self, board, extras=None):
#         return self.strategyMethod(board, extras)
#     # Strategies
#     def userInput(self, board, extras=None):
#         keypress=input("which way (wasd)?")
#         return keypress
#     def neuralNet(self, board, extras):
#         return getActionFromArray(arraySum(extras.predict(encodeboard(board, (28,28)))))
# class coach:
#     def __init__(self, continueconditions, rewardalgorithm):
#         self.keepTrying=getattr(self, continueconditions)
#         self.reward=getattr(self, rewardalgorithm)
#         self.reachedConditions={}
#     # Reward Algorithms
#     def percentReward(self, heuristics):
#         return heuristics['percentSolved']
#     # Continue Conditions
#     def stopWhenLoop(self, game):
#         return game.heuristics['isLoop'] or game.heuristics['isWon']
#     def randomReachedBoard(self):
#         return random.choice(list(self.reachedConditions.values()))[2]
#     def toString(self):
#         return str(self.reachedConditions)
#     def addToReached(self, game):
#         self.reachedConditions[game.toString()]=[game.commandHistory,game.heuristics['percentSolved'], game.board]

# def playGame(game_, strategy, coach, model):
#     max_=coach.reward(game_.heuristics)
#     coach.addToReached(game_)
#     while not coach.reward(game_.heuristics)==1:
#         if coach.reward(game_.heuristics)>max_:
#             max_=coach.reward(game_.heuristics)
#             coach.addToReached(game_)
#         print(max_)
#         while not coach.keepTrying(game_):
#             # print(game_.toString())
#             # print(game_.heuristics)
#             action=strategy.apply(game_.board, model)
#             # print(action)
#             game_.process(action)
#             # print(game_.commandHistory)
#         newboard=coach.randomReachedBoard()
#         game_=game(newboard)
#         # print(game_.toString())
#         # print(game_.heuristics)
#     return coach.reward(game_.heuristics)

# example=game(board)
# criticalstates={copy.deepcopy(example).toString():copy.deepcopy(example)}
# while example.heuristics['percentSolved']!=1:
#     oldPercentSolved=example.heuristics['percentSolved']
#     print(oldPercentSolved)
#     while not example.heuristics['isLoop']:
#         if oldPercentSolved<example.heuristics['percentSolved']:
#             oldPercentSolved=example.heuristics['percentSolved']
#             criticalstates[example.toString()]=copy.deepcopy(example)
#             break
#         # print(example.toString())
#         # print(example.commandHistory)
#         action=getActionFromArray(arraySum(model.predict(encodeboard(example.board, (28,28)))))
#         example.process(action)
#     # print(example.toString())
#     if example.heuristics['percentSolved']==1:
#         break
#     example=copy.deepcopy(random.choice(list(criticalstates.values())))
# trace(game(board),example.commandHistory)
# print(example.toString())
# print(example.commandHistory)

# strategy=strategy("neuralNet")
# coach=coach("stopWhenLoop","percentReward")
# playGame(example, strategy, coach, model)
# print(coach.toString())

# print(example.toString())
# print(example.findPerson())

# while(True):
#     keypress=input("which way (wasd)?")
#     example.process(keypress)
#     # if keypress=="w":
#     #     example.up()
#     # elif keypress=="a":
#     #     example.left()
#     # elif keypress=="s":
#     #     example.down()
#     # else:
#     #     example.right()
#     print(example.toString())
#     # print(example.findPerson())
#     print(str(example.percentSolved())+"%")
#     print(example.heuristics)
#     print(example.commandHistory)