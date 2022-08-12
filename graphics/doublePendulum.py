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
        self.tetha2 = math.radians(20)
        self.origin = (scrW / 2, 40)
        self.p_len = scrH / 4
        self.p_len2 = scrH / 5
        self.bob = (self.origin[0], self.p_len)
        self.bob2 = (self.bob[0], self.p_len2)
        self.acc1 = 0
        self.vel1 = 0
        self.acc2 = 0
        self.vel2 = 0
        self.m1 = 0.05
        self.m2 = 0.05
        self.dt = 0.5

    def new_pos(self):
        new_x = math.sin(self.tetha)*self.p_len
        new_y = math.cos(self.tetha)*self.p_len
        self.bob = (self.origin[0]+new_x, self.origin[1]+new_y)
        new_x2 = math.sin(self.tetha2)*self.p_len2
        new_y2 = math.cos(self.tetha2)*self.p_len2
        self.bob2 = (self.bob[0]+new_x2, self.bob[1]+new_y2)

    def calc_pos(self):
        num1 = -g_force*(2*self.m1 + self.m2) * math.sin(self.tetha)
        num2 = -self.m2*g_force*math.sin(self.tetha - 2*self.tetha2)
        num3 = -2*math.sin(self.tetha-self.tetha2) * self.m2
        num4 = (self.vel2*self.p_len2 + self.vel1 * self.p_len*math.cos(self.tetha-self.tetha2))
        den1 = self.p_len*(2*self.m1 + self.m2 - self.m2*math.cos(2*self.tetha - 2*self.tetha2))
        self.acc1 = (num1 + num2 + num3*num4)/den1

        num1a = 2*math.sin(self.tetha-self.tetha2)
        num2a = self.vel1*self.p_len*(self.m1 + self.m2)
        num3a = g_force*(self.m1+self.m2)*math.cos(self.tetha)
        num4a = self.vel2*self.p_len2*self.m2*math.cos(self.tetha-self.tetha2)
        den1a = self.p_len2*(2*self.m1 + self.m2 - self.m2*math.cos(2*self.tetha - 2*self.tetha2))
        self.acc2 = (num1a*(num2a+num3a+num4a))/den1a

        self.vel1 += self.acc1*self.dt
        self.vel1 *= .995
        self.tetha += self.vel1*self.dt
        self.vel2 += self.acc2*self.dt
        self.vel2 *= .995
        self.tetha2 += self.vel2*self.dt

    def draw(self, scr):
        pygame.draw.line(scr, c_white, (self.origin[0] - 50, self.origin[1]), (self.origin[0] + 50,
                                                                               self.origin[1]), 5)
        pygame.draw.line(scr, c_gray, self.origin, self.bob, 2)
        pygame.draw.circle(scr, c_white, self.bob, 8)
        pygame.draw.line(scr, c_gray, self.bob, self.bob2, 2)
        pygame.draw.circle(scr, c_white, self.bob2, 8)

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

        pend.draw(scr)
        pend.calc_pos()
        pend.new_pos()
        pygame.draw.lines(scr, c_white, True, [(0, 0), (0, scrH - 2), (scrW - 2, scrH - 2), (scrW - 2, 0)],
                          2)

        pygame.display.flip()
        pygame.time.wait(60)


if __name__ == "__main__":
    main()
