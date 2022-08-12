import pygame
from random import randint
done = False
bSize = 8
board = [[0 for x in range(bSize)] for y in range(bSize)]
white = (255,255,255)
scrSize = 600

def nextMove(xx,yy,movex):
    if movex==1:
        xx=xx+1
        yy=yy+2
    elif movex==2:
        xx=xx+2
        yy=yy+1
    elif movex==3:
        xx=xx-1
        yy=yy+2
    elif movex==4:
        xx=xx-2
        yy=yy+1
    elif movex==5:
        xx=xx+1
        yy=yy-2
    elif movex==6:
        xx=xx+2
        yy=yy-1
    elif movex==7:
        xx=xx-1
        yy=yy-2
    elif movex==8:
        xx=xx-2
        yy=yy-1

    if xx<0 or xx>bSize-1 or yy<0 or yy>bSize-1 or board[xx][yy]!=0:
        xx=-1
        yy=-1
    return [xx,yy]

def moveKnight(px,py,nn):
    board[px][py]=nn 
    if nn==bSize*bSize:
        gfxBoard()
        ddd=1
    else:
        for ii in range(1,8):
            newPos = nextMove(px,py,ii)
            if newPos[0]!=-1:              
                moveKnight(newPos[0],newPos[1],nn+1)
                board[newPos[0]][newPos[1]]=0       

def gfxBoard():
    scr = pygame.display.set_mode((scrSize,scrSize))
    pygame.init()
    scr.fill((0, 0, 0))
    for ii in range(1,bSize):
        pygame.draw.line(scr, white, (0,ii*(scrSize/bSize)), (scrSize,ii*(scrSize/bSize)),1)
        pygame.draw.line(scr, white, (ii*(scrSize/bSize),0), (ii*(scrSize/bSize),scrSize),1)
    fontx = pygame.font.SysFont("comicsansms", 60)
    for i in range(bSize):
        for j in range(bSize):
            if board[i][j]!=0:
                if board[i][j]==bSize*bSize:
                    text = fontx.render(str(board[i][j]), True, (100, 100, 255))
                else:
                    text = fontx.render(str(board[i][j]), True, (255, 255, 255))
                scr.blit(text,(i*scrSize/bSize + (scrSize/bSize/2 - text.get_width()/2) ,j*scrSize/bSize))
    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

def main():   
    #startx = randint(0,bSize-1)
    #starty = randint(0,bSize-1)
    startx=0
    starty=0
    for i in range(bSize):
        for j in range(bSize):
            board[i][j]=0

    moveKnight(startx,starty,1)       

main()
