import numpy as np

class game:
    def __init__(self, board):
        self.board=board
        self.reset()
        self.stateHistory={self.toString():""}
        self.commandHistory=["start"]
        self.commandLookup={"a":"left","w":"up", "s":"down", "d":"right"}
        self.heuristics={"isLoop": False, "isWon": False, "numDotsDone": 0, "numMoves":0, "percentSolved": self.percentSolved()}
    def reset(self):
        self.person=self.findPerson()
    def toString(self):
        grid=""
        for row in self.board:
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
    def findPerson(self):
        i=0
        for row in self.board:
            j=0
            for entry in row:
                if entry==11 or entry==21:
                    return [i,j]
                j+=1
            i+=1
    def left(self):
        # print("z")
        # print(self.board[self.person[0]][self.person[1]-1])
        # if self.board[self.person[0]][self.person[1]-1]!=0 and self.board[self.person[0]][self.person[1]-1]<10:
        #     print("a")
        #     self.board[self.person[0]][self.person[1]]=int((self.board[self.person[0]][self.person[1]]-self.board[self.person[0]][self.person[1]]%10)/10)
        #     self.board[self.person[0]][self.person[1]-1]=self.board[self.person[0]][self.person[1]-1]*10+1
        #     print(self.board[self.person[0]][self.person[1]],self.board[self.person[0]][self.person[1]-1] )
        # self.reset()
        self.move(self.person, [self.person[0],self.person[1]-1])
    def right(self):
        # print("z")
        # print(self.board[self.person[0]][self.person[1]+1])
        # if self.board[self.person[0]][self.person[1]+1]!=0 and self.board[self.person[0]][self.person[1]+1]<10:
        #     print("a")
        #     self.board[self.person[0]][self.person[1]]=int((self.board[self.person[0]][self.person[1]]-self.board[self.person[0]][self.person[1]]%10)/10)
        #     self.board[self.person[0]][self.person[1]+1]=self.board[self.person[0]][self.person[1]+1]*10+1
        #     print(self.board[self.person[0]][self.person[1]],self.board[self.person[0]][self.person[1]+1] )
        # self.reset()
        self.move(self.person, [self.person[0],self.person[1]+1])
    def down(self):
        # print("z")
        # print(self.board[self.person[0]+1][self.person[1]])
        # if self.board[self.person[0]+1][self.person[1]]!=0 and self.board[self.person[0]+1][self.person[1]]<10:
        #     print("a")
        #     self.board[self.person[0]][self.person[1]]=int((self.board[self.person[0]][self.person[1]]-self.board[self.person[0]][self.person[1]]%10)/10)
        #     self.board[self.person[0]+1][self.person[1]]=self.board[self.person[0]+1][self.person[1]]*10+1
        #     print(self.board[self.person[0]][self.person[1]],self.board[self.person[0]][self.person[1]+1] )
        # self.reset()
        self.move(self.person, [self.person[0]+1,self.person[1]])
    def up(self):
        # print("z")
        # print(self.board[self.person[0]-1][self.person[1]])
        # if self.board[self.person[0]-1][self.person[1]]!=0 and self.board[self.person[0]-1][self.person[1]]<10:
        #     print("a")
        #     self.board[self.person[0]][self.person[1]]=int((self.board[self.person[0]][self.person[1]]-self.board[self.person[0]][self.person[1]]%10)/10)
        #     self.board[self.person[0]-1][self.person[1]]=self.board[self.person[0]-1][self.person[1]]*10+1
        #     print(self.board[self.person[0]][self.person[1]],self.board[self.person[0]][self.person[1]+1] )
        # self.reset()
        self.move(self.person, [self.person[0]-1,self.person[1]])

    def move(self, start, end, isperson=True):
        # print("z")
        # print(self.board[start[0]][start[1]])
        startvalue=self.board[start[0]][start[1]]
        endvalue=self.board[end[0]][end[1]]
        if endvalue==10 or endvalue==20:
            if isperson==True:
                self.move(end, [2*end[0]-start[0], 2*end[1]-start[1]], False)
            else:
                return #False
        startvalue=self.board[start[0]][start[1]]
        endvalue=self.board[end[0]][end[1]]
        # print("aardvark")
        # print(startvalue, endvalue)
        if endvalue!=0 and endvalue<10:
            # print("a")
            if isperson:
                value=1
            else:
                value=0
            # print("ekans")
            self.board[start[0]][start[1]]=int((startvalue-startvalue%10)/10)
            self.board[end[0]][end[1]]=endvalue*10+value#1
            # print(startvalue,endvalue)
            
        else: 
            return #False
        self.reset()

    # method similar to https://github.com/JoshVarty/AlphaZeroSimple/blob/master/game.py 
    def get_reward_for_player(self):
        if self.isWon():
            return 1
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
        return [(cords[0] + 1, cords[1]), (cords[0] - 1, cords[1]), (cords[0], cords[1] + 1), (cords[0], cords[1] - 1)]
    def get_valid_moves(self):
        cords = self.findPerson()
        validMoves = self.validCords(cords)
        
        # everything is an invalid move by making np array 
        #for validMoves, mark i, j as 1
        newBoard = np.zeros((self.board.shape))
        for (x, y) in validMoves:
            newBoard[x][y] = 1
        return newBoard
        


    def isWon(self):
        for row in self.board:
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