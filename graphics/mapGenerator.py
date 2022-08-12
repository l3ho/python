from random import randint
import pygame
import math

cWhite = (255,255,255)
cBlue = (0, 90, 160)
cOrange = (255, 100, 0)
cGray = (50,50,50)
cGreen = (0, 160, 0)
mWidth,mHeight = 1800,900
arX = 0
arY = 0
mapAr = []
seedList = []

def drawMap(scra, mapArx,sqrSize):
    for i in range(arX):
        for j in range(arY):
            if mapArx[i][j]!=0 and mapArx[i][j]!=2:
                pygame.draw.rect(scra,cGreen,pygame.Rect(i*sqrSize,j*sqrSize,sqrSize,sqrSize))
            elif mapArx[i][j]==2:
                pygame.draw.rect(scra,cOrange,pygame.Rect(i*sqrSize,j*sqrSize,sqrSize,sqrSize))
            elif mapArx[i][j]==3:
                pygame.draw.rect(scra,cWhite,pygame.Rect(i*sqrSize,j*sqrSize,sqrSize,sqrSize))
            else:
                pygame.draw.rect(scra,cBlue,pygame.Rect(i*sqrSize,j*sqrSize,sqrSize,sqrSize))


def genSeeds(seedsX):
    for i in range(seedsX):
        px = randint(2,arX-2)
        py = randint(2,arY-2)
        mapAr[px][py]=2
        seedList.append((px,py))

def vLength(p1,p2):
    return int(math.sqrt(math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2)))

def findGropus(px,seedListx,p_groupx,seedDist):
    for sd in seedListx:
        dist = vLength(px,sd)
        if dist<=seedDist and isInGroup(sd,p_groupx)==False:
            p_groupx.append(sd)
            findGropus(sd,seedListx,p_groupx,seedDist)

def isInGroup(px, p_groupx):
    retFlag = False
    for pp in p_groupx:
        if pp == px:
            retFlag=True
            break
    return retFlag

def createGroups(p_groups,seedDistx):
    p_group=[]
    tmpSeeds = seedList
    p_group.append(seedList[0])
    ii=0
    while len(tmpSeeds)>0:
        findGropus(seedList[0],tmpSeeds,p_group,seedDistx)
        if p_group!=[] and len(p_group)>=1:
            p_groups.append(p_group)
        for pp in p_group:
            tmpSeeds.remove(pp)
        p_group=[]

def connectGroups(grps, scrx):
    for grp in grps:
        if len(grp)>2:
            pygame.draw.polygon(scrx, cGreen, grp, 0)
        elif len(grp)==2:
            pygame.draw.line(scrx, cGreen, grp[0], grp[1], 1)
        else:
            pygame.draw.line(scrx, cGreen, grp[0], grp[0], 1)   

def randomize(tmap,limit):
    newAr = tmap.copy()
    for i in range(arX):
        for j in range(arY):
            if tmap[i][j]!=0 and j>0 and j<arY-1:
                if tmap[i][j-1]==0 or tmap[i][j+1]==0:
                    ff=randint(1,limit)
                    if tmap[i][j-1]==0:
                        ff=-ff
                        for k in range(ff,0):
                            if j+k>=0:
                                newAr[i,j+k]=1
                    if tmap[i][j+1]==0:
                       for k in range(0,ff):
                           if j+k<arY:
                               newAr[i,j+k]=1
            if tmap[i][j]!=0 and i>0 and i<arX-1:
                if tmap[i+1][j]==0 or tmap[i-1][j]==0:
                    ff=randint(1,limit)
                    if tmap[i-1][j]==0:
                        ff=-ff
                        for k in range(ff,0):
                            if i+k>=0:
                                newAr[i+k,j]=1
                    if tmap[i+1][j]==0:
                       for k in range(0,ff):
                           if i+k<arX:
                               newAr[i+k,j]=1
    return newAr                   

def smoothEdgesY(tmap):
    limit = 2
    newAr = tmap.copy()
    edges = []
    for i in range(arX-1):
        for j in range(arY-limit):
            if tmap[i][j]!=0 and j>0 and j<arY:
                #top peaks
                if tmap[i][j-1]==0:
                    check = True
                    for k in range(1,limit):
                        if not(tmap[i-1][j+k]==0 and tmap[i+1][j+k]==0 and newAr[i,j+k]!=0):
                            check = False
                    if check == True:
                        for k in range(0,limit):
                            newAr[i,j+k]=0
                    else:        
                        #top valleys
                        check = True
                        for k in range(1,limit):
                            if not(tmap[i-1][j-k]==1 and tmap[i+1][j-k]==1 and newAr[i,j-k]!=1):
                                check = False
                        if check == True:
                            for k in range(1,limit):
                                newAr[i,j-k]=1
                #bottom peaks                
                if tmap[i][j+1]==0:
                    check = True
                    for k in range(1,limit):
                        if not(tmap[i-1][j-k]==0 and tmap[i+1][j-k]==0 and newAr[i,j-k]!=0):
                            check = False
                    if check == True:
                        for k in range(0,limit):
                            newAr[i,j-k]=0
                    else:        
                        #bottom valleys
                        check = True
                        for k in range(1,limit):
                            if not(tmap[i-1][j+k]==1 and tmap[i+1][j+k]==1 and newAr[i,j+k]!=1):
                                check = False
                        if check == True:
                            for k in range(1,limit):
                                newAr[i,j+k]=1                
    return newAr

def smoothEdgesX(tmap):
    limit = 2
    newAr = tmap.copy()
    edges = []
    for i in range(arX-1):
        for j in range(arY-limit):
            if tmap[i][j]!=0 and j>0 and j<arY:
                #left peaks
                if tmap[i-1][j]==0:
                    check = True
                    for k in range(1,limit):
                        if not(tmap[i+k][j-1]==0 and tmap[i+k][j+1]==0 and newAr[i+k,j]!=0):
                            check = False
                    if check == True:
                        for k in range(0,limit):
                            newAr[i+k,j]=0
                    else:        
                        #top valleys
                        check = True
                        for k in range(1,limit):
                            if not(tmap[i-k][j-1]==1 and tmap[i-k][j+1]==1 and newAr[i-k,j]!=1):
                                check = False
                        if check == True:
                            for k in range(1,limit):
                                newAr[i-k,j]=1
                #bottom peaks                
                if tmap[i+1][j]==0:
                    check = True
                    for k in range(1,limit):
                        if not(tmap[i-k][j-1]==0 and tmap[i-k][j+1]==0 and newAr[i-k,j]!=0):
                            check = False
                    if check == True:
                        for k in range(0,limit):
                            newAr[i-k,j]=0
                    else:        
                        #bottom valleys
                        check = True
                        for k in range(1,limit):
                            if not(tmap[i+k][j-1]==1 and tmap[i+k][j+1]==1 and newAr[i+k,j]!=1):
                                check = False
                        if check == True:
                            for k in range(1,limit):
                                newAr[i+k,j]=1                
    return newAr 

def gradientEdges(tmap, scrx,sqrSize):
    #cGreen = (0, 160, 0)
    cYellow = (210,181,91)
    ff=4
    for i in range(arX-1):
        for j in range(arY-1):
            if tmap[i][j]!=0:
                if tmap[i][j-1]==0 or tmap[i][j+1]==0:
                    if tmap[i][j-1]==0:
                        for k in range(0,ff):
                            if j+k<arY:
                                if tmap[i][j+k]!=0:
                                    tmpCol = (210-int(210*k/ff),181-int((181-160)*k/ff),91-int(91*k/ff))
                                    pygame.draw.rect(scrx,tmpCol,pygame.Rect(i*sqrSize,(j+k)*sqrSize,sqrSize,sqrSize))  
                    if tmap[i][j+1]==0:
                       for k in range(0,ff):
                           if j-k>=0:
                                if tmap[i][j-k]!=0:
                                    tmpCol = (210-int(210*k/ff),181-int((181-160)*k/ff),91-int(91*k/ff))
                                    pygame.draw.rect(scrx,tmpCol,pygame.Rect(i*sqrSize,(j-k)*sqrSize,sqrSize,sqrSize))
                if tmap[i-1][j]==0 or tmap[i+1][j]==0:
                    if tmap[i-1][j]==0:
                        for k in range(0,ff):
                            if i+k<arX:
                                if tmap[i+k][j]!=0:
                                    tmpCol = (210-int(210*k/ff),181-int((181-160)*k/ff),91-int(91*k/ff))
                                    pygame.draw.rect(scrx,tmpCol,pygame.Rect((i+k)*sqrSize,j*sqrSize,sqrSize,sqrSize))                       
                    if tmap[i+1][j]==0:
                        for k in range(0,ff):
                            if i-k>=0:
                                if tmap[i-k][j]!=0:
                                    tmpCol = (210-int(210*k/ff),181-int((181-160)*k/ff),91-int(91*k/ff))
                                    pygame.draw.rect(scrx,tmpCol,pygame.Rect((i-k)*sqrSize,j*sqrSize,sqrSize,sqrSize))             

def main():
    pygame.init()
    global mapAr,  arX, arY
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((mWidth, mHeight))
    rlimit = 3
    sqrSize = 3
    seedDist = 65
    seedsN = 60
    arX = int(mWidth/sqrSize)
    arY = int(mHeight/sqrSize)
    mapAr = [[0 for x in range(arY)] for y in range(arX)]
    
    genSeeds(seedsN)
    p_groupsx = []
    createGroups(p_groupsx,seedDist)

    done = False
    cntr = 1

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True   
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if cntr == 1:
                        scr = pygame.display.set_mode((arX,arY))
                        connectGroups(p_groupsx,scr)
                        mapAr = pygame.surfarray.array2d(scr)
                        scr = pygame.display.set_mode((mWidth, mHeight))
                    elif cntr == 2:
                        for ii in range(8):
                            mapAr = randomize(mapAr,rlimit)               
                    elif cntr == 3:
                        mapAr = smoothEdgesY(mapAr)
                        mapAr = smoothEdgesX(mapAr)
                        mapAr = smoothEdgesY(mapAr)
                        mapAr = smoothEdgesX(mapAr)
                    cntr+=1

        scr.fill((0, 0, 0))
        drawMap(scr,mapAr,sqrSize)
        if cntr ==5:
            gradientEdges(mapAr,scr,sqrSize)
        
        pygame.display.flip()
        #clock.tick(10)

main()