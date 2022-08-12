xSize, ySize = 800,800
fSize = 5
allFlakes=[]
buildup=[]
white = (255,255,255)
orange = (255,100,0)
import pygame
from random import randint

class snowFlake:
    posx=0
    posy=0
    vx=0
    vy=0

def initFlakes(platek):
        xx=randint(1,xSize)
        vxx=randint(-2,2)
        vyy=randint(2,4)
        platek.posx=xx
        platek.posy=0
        platek.vx=vxx
        platek.vy=vyy
                
        return platek

def moveFlake(flx):
    flx.posx = flx.posx+flx.vx
    flx.posy = flx.posy+flx.vy
    #check buildup
    for bb in range(1,len(buildup)-1):
            if flx.posy>ySize - buildup[bb] * fSize:
                if (flx.posx<bb * fSize + fSize and flx.posx>bb * fSize):
                    if buildup[bb-1]<buildup[bb] and abs(buildup[bb-1]-buildup[bb])<=1:
                        buildup[bb-1]+=1
                    elif buildup[bb+1]>buildup[bb] and abs(buildup[bb+1]-buildup[bb])<=1:
                        buildup[bb+1]+=1
                    elif buildup[bb+1]==buildup[bb] or buildup[bb-1]==buildup[bb]:
                        buildup[bb] += 1       

    if flx.posx<0 or flx.posx>xSize or flx.posy>ySize:
        initFlakes(flx)

    return flx

pygame.init()
clock = pygame.time.Clock()

flakes = 40
for xx in range(flakes):
    flake_x = snowFlake()
    initFlakes(flake_x)
    allFlakes.append(flake_x)

for xx in range(int(xSize/fSize)):
    buildup.append(1)

scr = pygame.display.set_mode((xSize,ySize))
done = False

while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        scr.fill((0, 0, 0))
        for flake_x in allFlakes:
            pygame.draw.rect(scr,white,pygame.Rect(flake_x.posx,flake_x.posy,fSize,fSize))
            moveFlake(flake_x)
        
        for aa in range(len(buildup)):
            for bb in range(1,buildup[aa]+1):
                recx=aa*fSize
                recy=ySize-bb*fSize
                pygame.draw.rect(scr,white,pygame.Rect(recx,recy,fSize,fSize))

        pygame.display.flip()
        clock.tick(60)
        

        

