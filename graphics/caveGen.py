import pygame
import numpy as np
import math
import noise

c_white = (255, 255, 255)
c_gray = (200, 200, 200)
c_black = (0, 0, 0)
c_blue = (255, 0, 0)
scrH = 800
scrW = 800
sbar_size = 200
p_height = 15
p_width = 5
grav = 3


class Player:
    def __init__(self, xx, yy):
        self.xx = xx
        self.yy = yy
        self.x_vel = 3
        self.jump = 30
        self.jump_falg = False

    def draw(self, scr):
        pygame.draw.rect(scr, c_blue, (self.xx, self.yy, p_width, p_height))

    def move(self, input):
        if input == 1:
            # left
            self.xx -= self.x_vel
        elif input == 2:
            #right
            self.xx += self.x_vel
        elif input == 3 and self.jump_falg is False:
            self.yy -= self.jump
            self.jump_falg = True
        self.yy += grav

def genCaveNoise():
    scale = 90.0
    octaves = 4
    persistence = 3.0
    lacunarity = 0.95
    cave = np.zeros((scrW, scrH))
    for i in range(scrW):
        for j in range(scrH):
            cave[i][j] = noise.pnoise2(i / scale, j / scale, octaves, persistence, lacunarity, 800, 800, 3)
    return cave


def convertCave(cave):
    caveRGB = np.zeros((scrW, scrH, 3))
    minVal = np.min(cave)
    maxVal = np.max(cave)
    midVal = minVal + (maxVal - minVal) / 1.9
    for i in range(scrW):
        for j in range(scrH):
            if cave[i][j] <= midVal:
                caveRGB[i][j][0] = c_black[0]
                caveRGB[i][j][1] = c_black[1]
                caveRGB[i][j][2] = c_black[2]
            else:
                caveRGB[i][j][0] = c_gray[0]
                caveRGB[i][j][1] = c_gray[1]
                caveRGB[i][j][2] = c_gray[2]
    return caveRGB


def main():
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((scrW + sbar_size, scrH))
    cave0 = genCaveNoise()
    cave0 = convertCave(cave0)
    surface = pygame.surfarray.make_surface(cave0)
    plr_status = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            plr = Player(x, y)
            plr_status = True

        scr.fill(c_black)
        scr.blit(surface, (0, 0))
        if plr_status:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]: plr.move(1)
            if pressed[pygame.K_RIGHT]: plr.move(2)
            if pressed[pygame.K_SPACE]:
                plr.move(3)
            plr.move(0)
            plr.check_collisions(cave0)
            plr.draw(scr)

        pygame.display.flip()
        pygame.time.wait(40)


if __name__ == "__main__":
    main()
