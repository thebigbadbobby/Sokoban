import numpy as np
#   Wall  = 0
#   Space = 1
#   Dot   = 2
#   Crate = _0
#   Person= _1

class game:
    def __init__(self, board):
        self.board=board
        self.reset()
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
        print("z")
        print(self.board[self.person[0]][self.person[1]-1])
        if self.board[self.person[0]][self.person[1]-1]!=0 and self.board[self.person[0]][self.person[1]-1]<10:
            print("a")
            self.board[self.person[0]][self.person[1]]=int((self.board[self.person[0]][self.person[1]]-self.board[self.person[0]][self.person[1]]%10)/10)
            self.board[self.person[0]][self.person[1]-1]=self.board[self.person[0]][self.person[1]-1]*10+1
            print(self.board[self.person[0]][self.person[1]],self.board[self.person[0]][self.person[1]-1] )
        self.reset()
    def right(self):
        print("z")
        print(self.board[self.person[0]][self.person[1]+1])
        if self.board[self.person[0]][self.person[1]+1]!=0 and self.board[self.person[0]][self.person[1]+1]<10:
            print("a")
            self.board[self.person[0]][self.person[1]]=int((self.board[self.person[0]][self.person[1]]-self.board[self.person[0]][self.person[1]]%10)/10)
            self.board[self.person[0]][self.person[1]+1]=self.board[self.person[0]][self.person[1]+1]*10+1
            print(self.board[self.person[0]][self.person[1]],self.board[self.person[0]][self.person[1]+1] )
        self.reset()
board=[[1, 1, 0, 0, 0, 0, 0, 1],
       [0, 0, 0, 1, 1, 1, 0, 1],
       [0, 2,11,10, 1, 1, 0, 1],
       [0, 0, 0, 1,10, 2, 0, 1],
       [0, 2, 0, 0,10, 1, 0, 1],
       [0, 1, 0, 1, 2, 1, 0, 0],
       [0,10, 1,10,10,10, 2, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]]

example=game(board)
print(example.toString())
print(example.findPerson())
example.left()
print(example.toString())
print(example.findPerson())
example.right()
print(example.toString())
print(example.findPerson())
