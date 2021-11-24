class inversegame:
    def __init__(self, board):
        self.board=board
        self.reset()
        self.stateHistory={self.toString():""}
        self.commandHistory=["start"]
        self.commandLookup={"a":"left","w":"up", "s":"down", "d":"right","A":"leftPull","W":"upPull","S":"downPull","D":"rightPull"}
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
    def clearSet(self):
        set={""}
        i=0
        for row in self.board:
            j=0
            for entry in row:
                if entry==1:
                    print(type(set), type({str([i,j])}))
                    set=set|{str([i,j])}
                j+=1
            i+=1
        return set
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
    def leftPull(self):
        self.move(self.person, [self.person[0],self.person[1]-1], isPull=True)
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
    def rightPull(self):
        self.move(self.person, [self.person[0],self.person[1]+1], isPull=True)
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
    def downPull(self):
        self.move(self.person, [self.person[0]+1,self.person[1]], isPull=True)
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
    def upPull(self):
        self.move(self.person, [self.person[0]-1,self.person[1]], isPull=True)
    def move(self, start, end, isPull=False, isperson=True):
        trail=[2*start[0]-end[0],2*start[1]-end[1]]
        # print("z")
        # print(self.board[start[0]][start[1]], start[0], start[1])
        startvalue=self.board[start[0]][start[1]]
        endvalue=self.board[end[0]][end[1]]
        trailingvalue=self.board[trail[0]][trail[1]]
        # print(startvalue, endvalue, trailingvalue)
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
            if isPull and isperson and trailingvalue>2:
                self.move(trail, start, isPull=False, isperson=False)
        else: 
            return False
        self.reset()
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
        personcoords=self.findPerson()
        commandMethod = getattr(self, self.lookupCommand(awsd))
        print("command:", self.lookupCommand(awsd))
        commandMethod()
        if self.findPerson!=personcoords:
            self.commandHistory.append(self.lookupCommand(awsd))
        for heuristic in self.heuristics:
            heuristicMethod = getattr(self, heuristic)
            self.heuristics[heuristic]=heuristicMethod()
    def lookupCommand(self, awsd):
        try:
            return self.commandLookup[awsd]
        except:
            return awsd