import pygame
from random import randint
import numpy as np

c_white = (255, 255, 255)
c_gray = (200, 200, 200)
c_black = (0, 0, 0)
c_blue = (255, 0, 0)
scrH = 800
scrW = 800
max_particles = 150
snow_size = 2
wind = 0
grav = 3

class Buildup:
    def __init__(self, xx, yy):
        self.xx = xx
        self.yy = yy
        self.vx = randint(0, 2) - 1
        self.stopped = False

    def reset(self):
        self.xx = randint(10, int(scrW/snow_size)-10)
        self.yy = randint(0, 10)

    def bounds(self):
        if self.xx + self.vx < 0 or self.xx+self.vx > scrW/snow_size-1:
            self.reset()

    def move(self, arx):
        if self.yy < (scrH/snow_size)-1:
            if arx[self.yy+1][self.xx] == 0:
                movex = False
                first_pos = (self.xx, self.yy)
                for ii in range(1, grav+1):
                    if self.yy + ii < (scrH/snow_size)-1:
                        if self.xx < 0 or self.xx > scrW/snow_size-1:
                            self.reset()
                        if arx[self.yy+ii][self.xx] != 0:
                            arx[first_pos[1]][first_pos[0]] = 0
                            arx[self.yy][self.xx] = 1
                            movex = False
                            break
                        self.yy += 1
                        movex = True
                if movex is True:
                    aa=1
                    if arx[self.yy][self.xx+self.vx] == 0:
                        #self.xx += self.vx
                        arx[self.yy][self.xx] = 1
                        arx[first_pos[1]][first_pos[0]] = 0
                    elif arx[self.yy][self.xx] == 0:
                        arx[self.yy][self.xx] = 1
                        arx[first_pos[1]][first_pos[0]] = 0

            elif arx[self.yy][self.xx-1] == 0 and arx[self.yy+1][self.xx-1] == 0 and arx[self.yy+1][self.xx] != 0:
                arx[self.yy][self.xx] = 0
                self.xx -= 1
                self.yy += 1
                arx[self.yy][self.xx] = 1
            elif arx[self.yy][self.xx+1] == 0 and arx[self.yy+1][self.xx+1] == 0 and arx[self.yy+1][self.xx] != 0:
                arx[self.yy][self.xx] = 0
                self.xx += 1
                self.yy += 1
                arx[self.yy][self.xx] = 1

def draw(scr, posx, colorx):
    pygame.draw.rect(scr, colorx, (int(posx[0]*snow_size), int(posx[1]*snow_size), snow_size, snow_size))

def domek(scr, arx):
    pygame.draw.lines(scr, c_blue, True, [(scrW/2, scrH), (scrW/2, scrH-60), (scrW/2+90, scrH - 60), (scrW/2 + 90, scrH)], 2)
    max_x = int(scrW / snow_size)-1
    max_y = int(scrH / snow_size)-1

    for y in range(30):
        arx[max_y - y][int(max_x / 2)+1] = 2
        arx[max_y - y][int(max_x / 2) + 46] = 2

    for x in range(2, 47):
        arx[max_y-29][int(max_x / 2) + x] = 2


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fontx = pygame.font.SysFont("arial", 12)
    scr = pygame.display.set_mode((scrW, scrH))
    snow_buildup = []
    snow_arr = np.zeros((int(scrW/snow_size), int(scrH/snow_size)))
    cntr = 1
    domek(scr, snow_arr)
    for i in range(max_particles):
        px = randint(10, int(scrW/snow_size)-10)
        #px = 10
        py = randint(10, int(scrH/snow_size)-100)
        snow_arr[py][px] = 1
        snow_buildup.append(Buildup(px, py))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #scr.fill(c_black)
        pygame.draw.rect(scr, c_black, (scrW - 40, 0, 40, 20))

        # if cntr % 10 == 0:
        #     px = 200
        #     py = randint(10, 20)
        #     snow_arr[py][px] = 1
        #     snow_buildup.append(Buildup(px, py))
        #     px = 205
        #     snow_arr[py][px] = 1
        #     snow_buildup.append(Buildup(px, py))

        for sb in snow_buildup:
            pos1 = (sb.xx, sb.yy)
            sb.bounds()
            sb.move(snow_arr)
            pos2 = (sb.xx, sb.yy)
            if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
                draw(scr, pos2, c_white)
                draw(scr, pos1, c_black)
            else:
                aa=1
                sb.reset()

        text = fontx.render(str(len(snow_buildup)), True, (255, 255, 255))
        scr.blit(text, (scrW - text.get_width(), 0))

        pygame.display.flip()
        pygame.time.wait(20)
        cntr += 1


if __name__ == "__main__":
    main()
