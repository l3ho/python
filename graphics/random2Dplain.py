import noise
import numpy as np
#from PIL import Image
import pygame
from random import randint
import math

cWhite = (255,255,255)
cBlue = (0, 90, 160)
cYellow = (238, 214, 175)
cGray = (139,137,137)
cGreen = (0, 160, 0)

def calcGrad(w_size):
    center_x, center_y = w_size[0]// 2, w_size[1] // 2
    circle_grad = np.zeros(w_size)

    for y in range(w_size[0]):
        for x in range(w_size[1]):
            distx = abs(x - center_x)
            disty = abs(y - center_y)
            dist = math.sqrt(distx*distx + disty*disty)
            circle_grad[y][x] = float(dist)

    # get it between -1 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    circle_grad -= 0.5
    circle_grad *= 2.0
    circle_grad = -circle_grad

    # shrink gradient
    for y in range(w_size[0]):
        for x in range(w_size[1]):
            if circle_grad[y][x] > -0.2:
                circle_grad[y][x] *= 20

    # get it between 0 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    return circle_grad

def main():
    wSize = (800,800)
    scale = 190.0
    octaves = 6
    persistence = 0.7
    lacunarity=2.0

    screen = pygame.display.set_mode(wSize)
    square=pygame.Surface((1, 1))

    world = np.zeros(wSize, dtype=np.float32)
    circGrad = calcGrad(wSize)


    for i in range(wSize[0]):
        for j in range(wSize[1]):
            world[i][j]=noise.pnoise2(i/scale,j/scale,octaves,persistence,lacunarity,1024,1024,0)

    world_noise = np.zeros_like(world, dtype=np.float32)

    for i in range(wSize[0]):
        for j in range(wSize[1]):
            world_noise[i][j]=world[i][j]*circGrad[i][j]
            if world_noise[i][j] > -0.2:
                world_noise[i][j] *= 25

    max_grad = np.max(world_noise)
    world_noise = world_noise / max_grad

    for i in range (wSize[0]):
        for j in range (wSize[1]):
            if world_noise[i][j]>=0.9:
                colr = cGray
            elif world_noise[i][j]>=0.45 and world_noise[i][j]<0.9:   
                colr = cGreen
            elif world_noise[i][j]>=0.4 and world_noise[i][j]<0.45:
                colr = cYellow              
            elif world_noise[i][j]<0.4:
                colr = cBlue
            square.fill(colr)
            draw_me=pygame.Rect((i+1), (j+1), 1, 1)
            screen.blit(square,draw_me)
    pygame.display.flip()

    done = False
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
            
    #im = Image.fromarray((world*255).astype('uint8'),"L")
    #im.show()     
        
main()
