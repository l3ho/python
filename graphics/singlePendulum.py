import pygame
import math
c_white = (255, 255, 255)
c_gray = (200, 200, 200)
c_black = (0, 0, 0)
scrH = 800
scrW = 800
sbar_size = 200
g_force = 9.8

class Pendulum():
    def __init__(self):
        self.tetha = math.radians(60)
        self.origin = (scrW / 2, 40)
        self.p_len = scrH / 5
        self.bob = (self.origin[0], self.p_len)
        self.acc = 0
        self.vel = 0

    def new_pos(self):
        new_x = math.sin(self.tetha)*self.p_len
        new_y = math.cos(self.tetha)*self.p_len
        self.bob = (self.origin[0]+new_x, self.origin[1]+new_y)

    def calc_pos(self):
        self.acc = -(g_force/self.p_len) * math.sin(self.tetha)
        self.vel += self.acc
        self.vel *= .995
        self.tetha += self.vel

    def draw(self, scr):
        pygame.draw.line(scr, c_white, (self.origin[0] - 50, self.origin[1]), (self.origin[0] + 50,
                                                                               self.origin[1]), 5)
        pygame.draw.line(scr, c_gray, self.origin, self.bob, 2)
        pygame.draw.circle(scr, c_white, self.bob, 8)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((scrW + sbar_size, scrH))

    pend = Pendulum()
    pend.new_pos()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        scr.fill(c_black)
        pressed = pygame.key.get_pressed()
        pend.draw(scr)
        pend.calc_pos()
        pend.new_pos()
        pygame.draw.lines(scr, c_white, True, [(0, 0), (0, scrH - 2), (scrW - 2, scrH - 2), (scrW - 2, 0)],
                          2)

        pygame.display.flip()
        pygame.time.wait(60)


if __name__ == "__main__":
    main()
