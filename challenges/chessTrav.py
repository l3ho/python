import numpy as np
solutions = 0

def oneMove(board,  ePoint, newPos, nn):
    tmpPos=newPos.copy()
    global solutions
    if newPos == ePoint:
        solutions +=1
        #print(board)
    else:
        for i in range(0,2):
            if i == 0:
                #down
                tmpPos[0]=newPos[0]+1     
            elif i == 1:
                #right
                tmpPos[1]=newPos[1]+1 
            if tmpPos[0] <= ePoint[0] and tmpPos[1] <= ePoint[1]:
                board[tmpPos[0],tmpPos[1]]=nn
                oneMove(board,ePoint,tmpPos,nn+1)
                board[tmpPos[0],tmpPos[1]]=0
                tmpPos=newPos.copy()
            else:
                tmpPos=newPos.copy()

def main():
    boardSize = (8,8)
    startP = (2,2)
    destP = (2,7)
    board = np.zeros(boardSize)
    board[startP[0],startP[1]]=99
    board[destP[0],destP[1]]=100
    startL = list(startP)
    endL = list(destP)

    oneMove(board,endL,startL,1)

    print(solutions)

main()    
