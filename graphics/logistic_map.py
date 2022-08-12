import pygame
from random import randint
import numpy as np
import matplotlib.pyplot as plt
white = (255, 255, 255)
gray = (50, 50, 50)
green = (0, 255, 0)

def calc_map(r, x_n):
    return r*x_n*(1-x_n)

def plotResults(scr, par):
    for i in range(len(par)):
        pygame.draw.rect(scr, white, pygame.Rect(i(0), i(1), 1, 1))

def main():
    #pygame.init()
    #clock = pygame.time.Clock()
    bWidth = 600
    bHeight = 600
    #scr = pygame.display.set_mode((bWidth, bHeight))
    done = False
    xcor = []
    ycor = []
    rr = 2.5
    nn = 500
    y0 = 0.1
    xx = 0
    r_ar = []
    xn_ar = []

    for j in range(0, 10000):
        for i in range(0, nn):
            ycor.append(y0)
            yy = calc_map(rr, y0)
            y0 = yy
            xx = xx + 0.02
        rtmp = [rr for ii in range(nn-10, nn)]
        r_ar.append(rtmp)
        xn_ar.append(ycor[int(nn-10):nn])
        rr = rr+0.001
        ycor = []

    plt.plot(r_ar, xn_ar, 'bo', markersize=0.5)
    plt.show()

    # while not done:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             done = True
    #     plotResults(scr, points)
    #     scr.fill((0, 0, 0))
    #     pygame.display.flip()
    #     clock.tick(60)

main()