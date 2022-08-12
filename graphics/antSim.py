import pygame
from random import randint
import math
import os

scrSize = 800
cBlack = (0, 0, 0)
cWhite = (255, 255, 255)
cGray = (180, 180, 180)
cBlue = (0, 128, 255)
cOrange = (200, 100, 100)
ant_w = 6
ant_l = 20
ant_dist = 40

class Ant(pygame.sprite.Sprite):
    def __init__(self,  ant_x, ant_y, angle):
        super().__init__()
        self.vel = 7
        self.distance = 0
        self.angle = angle
        self.way_home = []
        self.way_home.append(((ant_x, ant_y), 0))
        self.way_counter = 0
        self.or_image = pygame.Surface([ant_l*2, ant_l*2], pygame.SRCALPHA)
        rect1 = pygame.Rect(ant_l/2+ant_w, ant_l, ant_w, ant_l)
        rect2 = pygame.Rect(ant_l/2+ant_w, ant_l, ant_w, int(ant_l/5))
        #self.or_image = pygame.Surface([ant_w, ant_l], pygame.SRCALPHA)
        #rect1 = pygame.Rect(0, 0, ant_w, ant_l)
        #rect2 = pygame.Rect(0, 0, ant_w, int(ant_l/5))
        fov_rect = pygame.Rect(0, 0, ant_l*2, ant_l)
        #pygame.draw.rect(self.or_image, cGray, fov_rect)
        pygame.draw.rect(self.or_image, cOrange, rect1)
        pygame.draw.rect(self.or_image, cWhite, rect2)
        self.image = self.or_image
        self.rect = self.image.get_rect()
        self.rect.center = (ant_x, ant_y)

    def update(self):
        self.image = pygame.transform.rotate(self.or_image, self.angle-90)
        self.rect.y = self.rect.y - round(self.vel * math.sin(math.radians(self.angle)), 2)
        self.rect.x = self.rect.x + round(self.vel * math.cos(math.radians(self.angle)), 2)
        if self.distance % 10 or self.distance == 0:
            self.way_counter += 1
            self.way_home.append((self.rect.center, self.way_counter))
        self.distance = self.distance + self.vel
        self.angle, self.distance = check_angles(self.rect.x, self.rect.y, self.angle, self.distance)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def check_angles(x_pos, y_pos, deg_angle, cur_dist):
    new_angle = deg_angle
    if (0 < deg_angle < 90 or 270 < deg_angle < 360) and x_pos + ant_l > scrSize:
        new_angle = randint(95, 265)
    if (0 < deg_angle < 180) and y_pos <= 0:
        new_angle = randint(185, 355)
    if (90 < deg_angle < 270) and x_pos <= 0:
        new_angle = randint(275, 445) % 360
    if (180 < deg_angle < 360) and y_pos + ant_l > scrSize:
        new_angle = randint(5, 175)
    # if new_angle != deg_angle:
    #     cur_dist = 0
    if cur_dist >= ant_dist and new_angle == deg_angle:
        new_ang = randint(0, 60) - 30
        new_angle = (new_angle + new_ang) % 360
        cur_dist = 0
    return new_angle, cur_dist

class AntColony(pygame.sprite.Sprite):
    def __init__(self,  acx, acy):
        super().__init__()
        self.radius = 20
        self.image = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, cBlue, (self.radius, self.radius), 20)
        self.rect = self.image.get_rect()
        self.rect.x = acx - self.radius
        self.rect.y = acy - self.radius

def main():
    pygame.init()
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2000, 30)
    scr = pygame.display.set_mode((scrSize, scrSize))
    fontx = pygame.font.SysFont("comicsansms", 20)
    nn = 10
    done = False
    ac_x = 400
    ac_y = 400
    all_sprites = pygame.sprite.Group()
    ant_sprites = []
    for i in range(nn):
        start_angle = randint(0, 360)
        tmp_ant = Ant(ac_x, ac_y, start_angle)
        all_sprites.add(tmp_ant)
        ant_sprites.append(tmp_ant)
    all_sprites.add(AntColony(ac_x, ac_y))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        scr.fill(cBlack)

        colls = pygame.sprite.groupcollide(all_sprites, all_sprites, False, False)

        for i in range(len(ant_sprites)):
            for j in range(len(ant_sprites[i].way_home)):
                pygame.draw.circle(scr, cGray, ant_sprites[i].way_home[j][0], 0)
        # text = fontx.render("x = " + str(ant1.rect.x), True, (255, 255, 255))
        # scr.blit(text, (scrSize - text.get_width(), 0))

        all_sprites.draw(scr)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)

main()