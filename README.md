# Q-Compete
### Introduction
This program generates two competing neural network models, one that is trained to create difficult sokobans, and
another that is trained to solve them. The models use Monte Carlo branching to find the solution based on a learned probability distrobution output from the network, which serves as the Q function when normalized. The Q function is the function that assigns an efficiency score to a State — Action pair. In order to develop an effective Q-function, the solution network is trained to yield a Q-score of 1 for State - Action pairs in the traceback of moves from all successful solutions. Similarly, the generation network is trained to yield a Q-score of 1 for all State-Action pairs for all sokobans that were unable to be solved within a threshhold number moves. That way, the solution network learns to give a higher Q-score for actions that lead to the sokoban being solved, whereas the generation network learns to give a higher Q-score for actions that create difficult sokobans.
### Training Diagram
<img width="1682" alt="Screen Shot 2021-11-17 at 9 12 35 AM" src="https://user-images.githubusercontent.com/17601102/142249416-901fb88c-0b96-4e00-8f37-37d931f88048.png">
<img width="235" alt="Screen Shot 2021-11-18 at 2 23 57 PM" src="https://user-images.githubusercontent.com/17601102/142506460-aed93db1-b4e8-49e1-ac23-358f36d85b39.png">

### Model
##### Policy Network

The neural network begins with a 28 x 28 matrix that represents the state of the board. Each entry is one-hot-encoded. The input is funneled into a 32 x 32 Conv2d array and increased in size to a 64x64 and then flattened into a 4096 parameter feedforward neural network that outputs a 4x1 matrix representing which of the actions to take.

<img width="716" alt="Screen Shot 2021-11-20 at 10 22 56 PM" src="https://user-images.githubusercontent.com/17601102/142752115-66f6e509-a69a-4d4e-b03c-2d239209d949.png">

##### Value Network
<img width="752" alt="Screen Shot 2021-11-20 at 10 47 42 PM" src="https://user-images.githubusercontent.com/17601102/142752661-9d930254-394d-400f-a984-6ba9f95415a8.png">



The value network is structured the same but with the feed forward network outputing a 1x1 scalar representing the estimated remaining tries until the puzzle is solved.

### Classes
##### Game
###### init(self, board) 
sets up the given board matrix with an empty history of actions and a pre-filled list of possible actions and tracks coordinates of the person
- return: N/A
###### reset(self)
updates coordinates of the person
###### toString(self)
transforms the board into printable, human-readable form
- return: string that looks like board
###### findPerson(self)
finds coordinates of the person
- return: coordinates of the person
###### *{action}() x4
moves person according to which direction the action is
- return: None
###### move(self, wherepersonstarts, wherepersonendsup, isPerson=True)
moves person and figures out if a crate needs to move also (hence the toggle on isPerson)
- return: None
###### isWon(self)
determines if board state is solved
- return: Boolean of if the state is solved
###### isLoop(self)
determines if board state has been reached previously
- return: Boolean of if this state has been reached before in the state history
###### numDotsDone(self)
determines how many dots have a crate on them
- return: number of solved crates
###### numMoves(self)
determines how many moves have occured since game initialization
- return: total move count
###### percentSolved(self)
determines what percent of dots have a crate on them
- return: percent of crates that are solved
###### process(self)
applies an action to a state, resulting in the next state
- return: 
###### lookupCommand(self, actionname)
searches the prefilled list of actions for a matching action name and returns the action that the inputted string is referring to.

##### InvGame
Same structure as Game but move() is the inverse and there are 8 possible actions instead of 4 because player has the option of pulling the crate in reverse or not.

### Files
##### Model
###### encodeboard(board, size)
encodes a board state into the format that the neural network takes as input (1, n, n, 1).
- return: board padded to be size x size matrix
###### arraySum(array)
normalizes model output to be turned into probabilities.
- return: normalized probability distribution (policy given the current state)
###### getActionFromArray(normprobarray)
decides which branch to take based on array weights.
- return: action derived from evaluation of probability distrobution
###### trace(game, commandHistory)
forensically finds all the board state action pairs taken after a successful attempt.
- return: TBD
###### encoder(inputsize, outputsize)
defines CNN model according to size constraints.
- return: keras CNN model


##### GenerateSamples
###### place_crates(rows, cols, boxes)
generates a random solved sokoban board state with no walls
- return: solved board matrix
###### generate_sokoban(model, rows, cols, boxes)
generates an unsolved sokoban puzzle using inversegame and a 9* action cnn model
- return: unsolved game object
##### SolveSamples
###### solve_sokoban()
solves a sokoban puzzle using game and a 4 action cnn mode, then returns how many moves it took to solve. Has a cutoff where it fails to solve at a certain point.
- return: number of moves it took to solve
##### TrainInverse
###### EvaluatePerformance()
initializes 2 cnn models and generates 10 sample sokobans then returns an array of how many moves the solver took to solve each
return: array of the number of moves attempted before finding the solution for each sample.



