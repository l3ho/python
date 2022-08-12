import noise
import numpy as np
import pygame

def main():
    pygame.init()
    clock = pygame.time.Clock()
    wSize = (800,500)
    scr = pygame.display.set_mode(wSize)
    scale = 90.0
    octaves = 3
    persistence = 0.3
    lacunarity = 2.0
    done = False

    world = np.zeros(wSize[0])

    for i in range(wSize[0]):
        world[i]=wSize[1]/2 + 200*noise.pnoise1(i/scale,octaves,persistence,lacunarity,800,0)
        #world[i]=noise.pnoise1(i/scale,octaves,persistence,lacunarity,800,0)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
        for i in range(wSize[0]):
            pygame.draw.line(scr,(255,255,255),(i,world[i]),(i,world[i]),1)

        pygame.display.flip()
        clock.tick(60)
        
main()
