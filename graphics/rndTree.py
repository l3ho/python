import pygame
from random import randint
white = (255, 255, 255)
gray = (50, 50, 50)
green = (0, 255, 0)

class branch:
    def __init__(self, startP):
        self.spl=0
        self.splFlag = False 
        self.brn = []
        self.brn.append(startP)
        self.vx = 0
    def add(self,x):
        self.brn.append(x)
    def lastP(self):
        return self.brn[len(self.brn)-1]
        
def nextMove(bx, xShift, yShift):
    retFlag = True
    xMove = randint(-xShift,xShift)
    yMove = randint(-yShift,-1)
    #check split limit
    lastPoint = bx.lastP()
    pTmp = (lastPoint[0]+xMove+bx.vx,lastPoint[1]+yMove)
    bx.add(pTmp)
    if bx.spl >= 30:
        newB = randint(0,2)
        if newB == 0:
            bx.splFlag = True
            bx.spl = 0
        else:
            bx.spl=0
    else:
        bx.spl+=1
    if pTmp[1]<=0:
        retFlag = False
    return retFlag
        
def drawTree(scrx, brs):
    for bb in brs:
        for kk in range(len(bb.brn)-1):
            pygame.draw.line(scrx,green,bb.brn[kk],bb.brn[kk+1],2)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    bWidth = 600
    bHeight = 600
    sqrSize = 2
    start_p = (bWidth/2-sqrSize/2,bHeight-sqrSize)
    scr = pygame.display.set_mode((bWidth, bHeight))
    done = False
    branches = []
    b1 = branch(start_p)
    branches.append(b1)
    vxx = 1
    cont = True
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        scr.fill((0, 0, 0))
        if cont == True:
            for br in branches:
                if nextMove(br,4,5)==True:
                    if br.splFlag == True:
                        bxx = branch(br.lastP())
                        if br.vx == 0:
                            br.vx = vxx
                            bxx.vx = -vxx
                        elif br.vx>0:
                            bxx.vx = - vxx
                        else:
                            bxx.vx = vxx
                        br.splFlag=False
                        branches.append(bxx)
                else:
                    branches.clear()
                    b1 = branch(start_p)
                    branches.append(b1)                

        drawTree(scr,branches)
       
        pygame.display.flip()
        clock.tick(60)

main()