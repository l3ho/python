import pygame
import numpy as np
import random
import math

white = (255, 255, 255)
gray = (70, 70, 70)
dark_gray = (10, 10, 10)
green = (0, 255, 0)
cBlack = (0, 0, 0)

def randomizeArea(gArea):
    for i in range(len(gArea)):
        for j in range(len(gArea[0])):
            gArea[i][j] = random.randint(0, 9)
            #gArea[i][j] = 15
    return gArea

def randomizePath(gArea, pointCount):
    maxX = len(gArea) - 1
    maxY = len(gArea[0]) - 1
    pathPoints = np.zeros((pointCount, 3))
    fullPath = []
    for i in range(pointCount):
        if i>0 and i<pointCount-1:
            pathPoints[i][0] = random.randint(2, len(gArea)-3)
            pathPoints[i][1] = random.randint(2, len(gArea[0]) - 3)
        elif i == pointCount - 1:
            pathPoints[i][0] = maxX
            pathPoints[i][1] = maxY
        elif i == 0:
            pathPoints[i][0] = 0
            pathPoints[i][1] = 0
        fullPath.append((pathPoints[i][0], pathPoints[i][1]))
        pathPoints[i][2] = math.sqrt((maxY - pathPoints[i][1])**2 + (maxX - pathPoints[i][0])**2)

    ind = np.argsort(pathPoints[:, -1])
    pathPoints = pathPoints[ind]
    y_val = 0
    x_val = 0
    p1 = (maxX, maxY)
    cor_val = decideCorridor(gArea[maxX][maxY], "u")
    gArea[maxX][maxY] = cor_val
    cor_val = decideCorridor(gArea[0][0], "l")
    gArea[0][0] = cor_val
    #create paths
    for kk in range(pointCount):
        for yy in range(abs(p1[1] - int(pathPoints[kk][1])+1)):
            if p1[1] > int(pathPoints[kk][1]):
                y_val = p1[1] - yy
                cor_val = decideCorridor(gArea[p1[0]][y_val], "d")
            else:
                y_val = int(pathPoints[kk][1]) - yy
                cor_val = decideCorridor(gArea[p1[0]][y_val], "u")
            gArea[p1[0]][y_val] = cor_val
            fullPath.append((p1[0], y_val))
        for xx in range(abs(p1[0] - int(pathPoints[kk][0]))+1):
            if p1[0] > int(pathPoints[kk][0]):
                x_val = p1[0] - (p1[0] - int(pathPoints[kk][0])) + xx
                cor_val = decideCorridor(gArea[x_val][int(pathPoints[kk][1])], "l")
            else:
                x_val = int(pathPoints[kk][0]) - (int(pathPoints[kk][0]) - p1[0]) + xx
                cor_val = decideCorridor(gArea[x_val][int(pathPoints[kk][1])], "r")
            gArea[x_val][int(pathPoints[kk][1])] = cor_val
            fullPath.append((x_val, int(pathPoints[kk][1])))
        p1 = (int(pathPoints[kk][0]), int(pathPoints[kk][1]))
    # for kk in range(pointCount):
    #    gArea[int(pathPoints[kk][0])][int(pathPoints[kk][1])] = -1
    return gArea, fullPath

def decideCorridor(original_value, direction):
    retVal = ""
    binStr = format(original_value, "04b")
    binVal = list(binStr)
    if direction == "u":
        binVal[0] = "0"
        binVal[2] = "0"
    elif direction == "l":
        binVal[1] = "0"
        binVal[3] = "0"
    elif direction == "d":
        binVal[0] = "0"
        binVal[2] = "0"
    elif direction == "r":
        binVal[3] = "0"
        binVal[1] = "0"
    return int(str(''.join(binVal)), 2)

def drawArea(screen, gArea, mPath, sWidth, sHeight):
    rectLine = 4
    for i in range(len(gArea)):
        for j in range(len(gArea[0])):
            binVal = format(gArea[i][j], "04b")
            if binVal[0] == "1":
                #top
                startPoint = (int(i * sWidth / len(gArea)), int(j * sHeight / len(gArea[0])))
                endPoint = (int((i+1) * sWidth / len(gArea)), int(j * sHeight / len(gArea[0])))
                pygame.draw.line(screen, gray, startPoint, endPoint, rectLine)
            if binVal[1] == "1":
                #left
                startPoint = (int(i * sWidth / len(gArea)), int(j * sHeight / len(gArea[0])))
                endPoint = (int(i * sWidth / len(gArea)), int((j+1) * sHeight / len(gArea[0])))
                pygame.draw.line(screen, gray, startPoint, endPoint, rectLine)
            if binVal[2] == "1":
                #down
                startPoint = (int(i * sWidth / len(gArea)), int((j+1) * sHeight / len(gArea[0])))
                endPoint = (int((i+1) * sWidth / len(gArea)), int((j+1) * sHeight / len(gArea[0])))
                pygame.draw.line(screen, gray, startPoint, endPoint, rectLine)
            if binVal[3] == "1":
                #right
                startPoint = (int((i+1) * sWidth / len(gArea)), int(j * sHeight / len(gArea[0])))
                endPoint = (int((i+1) * sWidth / len(gArea)), int((j+1) * sHeight / len(gArea[0])))
                pygame.draw.line(screen, gray, startPoint, endPoint, rectLine)

    for i in range(len(mPath)):
        tmpRect = pygame.Rect(int(mPath[i][0] * sWidth / len(gArea)) + 10, int(mPath[i][1] * sHeight / len(gArea[0]))
                              + 10, int(sWidth / len(gArea)) - 20, int(sWidth / len(gArea[0])) - 20)
        pygame.draw.rect(screen, dark_gray, tmpRect)

    roomRect = pygame.Rect(0, 0, int(sWidth - rectLine/2),
                           int(sHeight - 1))
    pygame.draw.rect(screen, white, roomRect, 4)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    random.seed(37)
    areaWidth = 10
    areaHeight = 10
    screenWidth = 800
    screenHeight = 800
    gameArea = np.zeros((areaWidth, areaHeight), dtype='uint8')
    scr = pygame.display.set_mode((screenWidth, screenHeight))

    maze = randomizeArea(gameArea)
    maze, maze_path = randomizePath(maze, 6)
    drawArea(scr, maze, maze_path, screenWidth, screenHeight)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # scr.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)


main()
