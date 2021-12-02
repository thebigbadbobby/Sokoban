import numpy as np
import copy
import time
class game:
    def __init__(self, board, row, col, maxrow, maxcol):
        self.board=board
        # self.reset()
        self.row = row 
        self.col = col
        self.maxrow = maxrow
        self.maxcol = maxcol
        # self.stateHistory={self.toString():""}
        self.commandHistory=["start"]
        self.commandLookup={"a":"left","w":"up", "s":"down", "d":"right"}
        self.heuristics={"isLoop": False, "isWon": False, "numDotsDone": 0, "numMoves":0, "percentSolved": self.percentSolved()}
    # def reset(self):
    #     self.person=self.findPerson()
    def getBoard(self):
        return self.board
    def string_representation(self):
        return np.array_str(self.board)
    def get_action_size(self):
        return self.board.shape[0] * self.board.shape[1]
    def toString(self, state):
        grid=""
        # board = self.board
        # board = board
        state = np.array(state).reshape(self.maxrow, self.maxcol)
        for row in state[:self.row]:
            for entry in row:
                if entry==0:
                    grid+="■"
                elif entry==1:
                    grid+=" "
                elif entry==2:
                    grid+="o"
                elif entry%10==0:
                    grid+="▤"
                elif entry%10==1:
                    grid+="☆"
            grid+="\n"
        return grid
    def findPerson(self, state):
        # state = state[:self.maxrow*self.maxcol]
        i=0
        # print(self.board)
        state = np.array(state).reshape(self.maxrow, self.maxcol)
        state = state[:self.row][:self.col]
        for row in state:
            j=0
            # print('row')
            # print(row)
            for entry in row:
                # print('entry')
                # print(entry)
                if entry==11 or entry==21:
                    return [i,j]
                j+=1
            i+=1
    def clearSet(self):
        set={''}
        i=0
        for row in self.board:
            j=0
            for entry in row:
                if entry==1:
                    # print(type(set), type({str([i,j])}))
                    set=set|{str([i,j])}
                j+=1
            i+=1
        return set

    def left(self, person, state):
        return self.move(person, [person[0],person[1]-1], state)

    def right(self, person, state):
        return self.move(person, [person[0],person[1]+1], state)

    def down(self, person, state):
        return self.move(person, [person[0]+1,person[1]], state)

    def up(self, person, state):
        return self.move(person, [person[0]-1,person[1]], state)

    def checkDouble(self):
        count = 0
        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.board[i][j] == 11:
                    count += 1
        if count > 1:
            print("THIS IS BAD")
            exit()

    def move(self, start, end, state, isperson=True):
        # print("z")
        # state = np.array(state).reshape(self.maxrow, self.maxcol)
        # state = state[:self.row][:self.col]
        state = np.array(state).reshape(self.maxrow, self.maxcol)
        # print('before')
        # print(self.toString(state))
        startvalue=state[start[0]][start[1]]
        endvalue=state[end[0]][end[1]]
        if endvalue==10 or endvalue==20:
            if isperson==True:
                state = self.move(end, [2*end[0]-start[0], 2*end[1]-start[1]],state, False)
                state = np.array(state).reshape(self.maxrow, self.maxcol)
            else:
                #this is when there's a second crate in front
                return np.ndarray.flatten(state)
        startvalue=state[start[0]][start[1]]
        endvalue=state[end[0]][end[1]]
        # print("aardvark")
        # print(startvalue, endvalue)
        #this is for the wall
        if endvalue!=0 and endvalue<10:
            # print("a")
            if isperson:
                value=1
            else:
                value=0
            # print("ekans")
            state[start[0]][start[1]]=int((startvalue-startvalue%10)/10)
            state[end[0]][end[1]]=endvalue*10+value#1
            # print(startvalue,endvalue)
        else:
            #if can't move cuz of box
            # print(self.toString(state))
            return np.ndarray.flatten(state)
        # print('after')
        # print(self.toString(state))
        return np.ndarray.flatten(state)

    # method similar to https://github.com/JoshVarty/AlphaZeroSimple/blob/master/game.py 
    def get_next_state(self, action, state,trainerMove=False):
        person = self.findPerson(state)
        if person[1] - 1 == action[1]:
            if trainerMove:
                print('left')
            return self.left(person, state)
        if person[1] + 1 == action[1]:
            if trainerMove:
                print('right')
            return self.right(person, state)
        if person[0] - 1 == action[0]:
            if trainerMove:
                print('up')
            return self.up(person, state)
        if person[0] + 1 == action[0]:
            if trainerMove:
                print('down')
            return self.down(person, state)
    def detectLock(self, state):
        state = np.array(state).reshape(self.maxrow, self.maxcol)
        state = state[:self.row][:self.col]
        for i in range(0, self.row):
            for j in range(0, self.col):
                if state[i][j] == 10:
                    # bottom left
                    if state[i][j-1] == 0 and state[i + 1][j] == 0:
                        return True
                    if state[i][j-1] == 20 and state[i + 1][j] == 0:
                        return True
                    if state[i][j-1] == 0 and state[i + 1][j] == 20:
                        return True
                    if state[i][j-1] == 20 and state[i + 1][j] == 20:
                        return True
                    # top right
                    if state[i][j+1] == 0 and state[i - 1][j] == 0:
                        return True
                    if state[i][j+1] == 20 and state[i - 1][j] == 0:
                        return True
                    if state[i][j+1] == 0 and state[i - 1][j] == 20:
                        return True
                    if state[i][j+1] == 20 and state[i - 1][j] == 20:
                        return True
                    #top left
                    if state[i][j-1] == 0 and state[i - 1][j] == 0:
                        return True
                    if state[i][j-1] == 20 and state[i - 1][j] == 0:
                        return True
                    if state[i][j-1] == 0 and state[i - 1][j] == 20:
                        return True
                    if state[i][j-1] == 20 and state[i - 1][j] == 20:
                        return True
                    #bottom right
                    if state[i][j+1] == 0 and state[i + 1][j] == 0:
                        return True
                    if state[i][j+1] == 20 and state[i + 1][j] == 0:
                        return True
                    if state[i][j+1] == 0 and state[i + 1][j] == 20:
                        return True
                    if state[i][j+1] == 20 and state[i + 1][j] == 20:
                        return True
        return False
    def get_reward_for_player(self, state):
        if self.isWon(state):
            return 1
        if self.detectLock(state):
            return 0
        else:
            return None # try this out, then try attempts out then try outright returning 0 for loss
    def validCords(self, cords):
        #top board
        if cords[0] == 0 and cords[1] == 0:
            return [(cords[0] + 1, cords[1]), (cords[0], cords[1] + 1)]
        if cords[0] == 0 and cords[1] == len(self.board[0]) - 1:
            return [(cords[0], cords[1] - 1), (cords[0] + 1, cords[1])]
        if cords[0] == 0 and not cords[1] == 0:
            return [(cords[0], cords[1] + 1), (cords[0], cords[1] - 1), (cords[0] + 1, cords[1])]

        #bottom board
        if cords[0] == len(self.board) - 1 and cords[1] == 0:
            return [(cords[0] - 1, cords[1]), (cords[0], cords[1] + 1)]
        if cords[0] == len(self.board) - 1 and cords[1] == len(self.board[0]) - 1:
            return([cords[0] - 1, cords[1], (cords[0], cords[1] - 1)])
        if cords[0] == len(self.board) - 1 and not cords[1] == 0:
            return[(cords[0] - 1, cords[1]), (cords[0], cords[1] - 1), (cords[0], cords[1] + 1)]
        
        #sides of the board
        if not cords[0] == 0 and cords[1] == 0:
            return [(cords[0] + 1, cords[1]), (cords[0] - 1, cords[1]), (cords[0], cords[1] + 1)]
        if not cords[0] == 0 and cords[1] == len(self.board[0]) - 1:
            return [((cords[0] + 1, cords[1]), (cords[0] - 1, cords[1]), (cords[0], cords[1] - 1))]
        
        #if your in the middle go up down left right
        # print('returning these')
        return [(cords[0] + 1, cords[1]), (cords[0] - 1, cords[1]), (cords[0], cords[1] + 1), (cords[0], cords[1] - 1)]
    def get_valid_moves(self, state):
        cords = self.findPerson(state)
        validMoves = self.validCords(cords)
        
        # everything is an invalid move by making np array 
        #for validMoves, mark i, j as 1
        newBoard = np.zeros((self.board.shape))
        for (x, y) in validMoves:
            newBoard[x][y] = 1
        return newBoard
    
    def checkValid(self, move, state):
        cords = self.findPerson(state)
        validMoves = self.validCords(cords)
        for vMove in validMoves:
            if move[0] == vMove[0] and move[1] == vMove[1]:
                return True

        return False
        


    def isWon(self, state):
        state = np.array(state).reshape(self.maxrow, self.maxcol)
        state = state[:self.row][:self.col]
        for row in state:
            for entry in row:
                if entry==10:
                    return False
        return True
    def isLoop(self):
        if self.toString() in self.stateHistory:
            return True
        else:
            self.stateHistory[self.toString()]=""
            return False
    def numDotsDone(self):
        count=0
        for row in self.board:
            for entry in row:
                if entry == 20:
                    count+=1
        return count
    def numMoves(self):
        return len(self.commandHistory)
    def percentSolved(self):
        solved=0
        unsolved=0
        for row in self.board:
            for entry in row:
                if entry==10:
                    unsolved+=1
                if entry==20:
                    solved+=1
        return solved/(unsolved+solved)
    def process(self, awsd):
        commandMethod = getattr(self, self.lookupCommand(awsd))
        print("command:", self.lookupCommand(awsd))
        commandMethod()
        self.commandHistory.append(self.lookupCommand(awsd))
        for heuristic in self.heuristics:
            heuristicMethod = getattr(self, heuristic)
            self.heuristics[heuristic]=heuristicMethod()
    def lookupCommand(self, awsd):
        try:
            return self.commandLookup[awsd]
        except:
            return awsd