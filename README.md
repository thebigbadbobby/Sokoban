# Q-Compete
### Introduction
This program generates two competing neural network models, one that is trained to create difficult sokobans, and
another that is trained to solve them. The models use Monte Carlo branching to find the solution based on a learned probability distrobution output from the network, which serves as the Q function when normalized. The Q function is the function that assigns an efficiency score to a State — Action pair. In order to develop an effective Q-function, the solution network is trained to yield a Q-score of 1 for State - Action pairs in the traceback of moves from all successful solutions. Similarly, the generation network is trained to yield a Q-score of 1 for all State-Action pairs for all sokobans that were unable to be solved within a threshhold number moves. That way, the solution network learns to give a higher Q-score for actions that lead to the sokoban being solved, whereas the generation network learns to give a higher Q-score for actions that create difficult sokobans.
### Diagram
<img width="1682" alt="Screen Shot 2021-11-17 at 9 12 35 AM" src="https://user-images.githubusercontent.com/17601102/142249416-901fb88c-0b96-4e00-8f37-37d931f88048.png">
<img width="235" alt="Screen Shot 2021-11-18 at 2 23 57 PM" src="https://user-images.githubusercontent.com/17601102/142506460-aed93db1-b4e8-49e1-ac23-358f36d85b39.png">

### Classes
##### Model
###### Encodeboard()
encodes a board state into the format that the neural network takes as input (1, n, n, 1).
###### arraySum()
normalizes model output to be turned into probabilities.
###### getActionFromArray()
decides which branch to take based on array weights.
###### trace()
forensically finds all the board state action pairs taken after a successful attempt.
###### encoder()
defines CNN model.

##### Game
###### init() 
sets up the given board with an empty history of actions and a pre-filled list of possible actions and tracks coordinates of the person
###### reset()
updates coordinates of the person
###### toString()
prints the board in human-readable form
###### findPerson()
finds coordinates of the person
###### *{action}() x4
moves person according to which direction the action is
###### move()
moves person and figures out if a crate needs to move also
###### isWon()
determines if board state is solved
###### isLoop()
determines if board state has been reached previously
###### numDotsDone()
determines how many dots have a crate on them
###### numMoves()
determines how many moves have occured since game initialization
###### percentSolved()
determines what percent of dots have a crate on them
###### process()
applies an action to a state, resulting in the next state
###### lookupCommand()
searches the prefilled list of actions for the action that the inputted string is referring to and returns that action

###### InvGame
Same as Game but moves are the inverse functions except there are 8 possible actions instead of 4.

### Files
##### GenerateSamples
###### generate_sokoban()
generates a sokoban puzzle using inversegame and a 9* action cnn model
##### SolveSamples
###### solve_sokoban()
solves a sokoban puzzle using game and a 4 action cnn mode, then returns how many moves it took to solve. Has a cutoff where it fails to solve at a certain point.
##### TrainInverse
###### EvaluatePerformance()
initializes 2 cnn models and generates 10 sample sokobans then returns an array of how many moves the solver took to solve each




