from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import noise
import numpy as np

cWhite = (255,255,255)
cBlue = (0, 90, 160)
cYellow = (238, 214, 175)
cGray = (70,70,70)
cGreen = (0, 160, 0)


def genNoise(wSize,flyX,flyY):
    scale = 100
    octaves = 7
    persistence = 0.8
    lacunarity=1.8
    world = np.zeros(wSize, dtype=np.float32)

    for i in range(wSize[0]):
        for j in range(wSize[1]):
            world[i][j]=noise.pnoise2(i/scale + flyX,(j/scale) + flyY,octaves,persistence,lacunarity,1024,1024,0)

    max_grad = np.max(world)
    world_noise = (world / max_grad)*2.0

    return world_noise    

def genPlain(wSize, flyX,flyY):
    scaleF=1.1

    zArray = genNoise(wSize,flyX,flyY)

    glBegin(GL_LINE_STRIP)

    for x in range(wSize[0]-1):
        for y in range(wSize[1]-1):
            glVertex3f(x*scaleF,y*scaleF,scaleF*zArray[x][y])
            glVertex3f((x+1)*scaleF,y*scaleF,scaleF*zArray[x+1][y])

    glEnd()


def main():
    pygame.init()
    size = (800,800)
    pScale = 20
    flyingX = 0.1
    flyingY = 0.0

    #zvalues = genNoise((int(size[0]/pScale),int(size[1]/pScale)))

    video_flags = pygame.OPENGL | pygame.DOUBLEBUF    
    screen = pygame.display.set_mode(size, video_flags)

    gluPerspective(45, (size[0]/size[1]), 0.2, 100.0)

    glTranslatef(-17,6, -40)
    glRotatef(120, 1, 0, 0)

    fSwitch=1


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()                    

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        genPlain((int(size[0]/pScale),int(size[1]/pScale)),flyingX,flyingY)
        pressed = pygame.key.get_pressed()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: fSwitch=-1
        if pressed[pygame.K_DOWN]: fSwitch=1  
        if pressed[pygame.K_LEFT]: flyingX -= 0.005 
        if pressed[pygame.K_RIGHT]:  flyingX += 0.005 
        flyingY -= 0.005 * fSwitch
        #flyingX -= 0.005 * fSwitch
        pygame.display.flip()
        pygame.time.wait(10)

 
if __name__ == "__main__":
    main()