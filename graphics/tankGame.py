import pygame
from random import randint
scrX,scrY = 400,600
cWhite = (255,255,255)
cBlue = (0, 128, 255)
cOrange = (255, 100, 0)
cBlack = (0,0,0)

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height],pygame.SRCALPHA)
        rect1 = pygame.Rect(0,height/2,width,height/2)
        rect2 = pygame.Rect(width/2-5,0,10,height/2)
        pygame.draw.rect(self.image,cBlue,rect1)
        pygame.draw.rect(self.image,cOrange,rect2)
        self.rect = self.image.get_rect() 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y-=3

def main(screenX, screenY):
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((screenX, screenY))
    font = pygame.font.SysFont("comicsansms", 20)
    done = False

    allSprites = pygame.sprite.Group()
    bulletList = pygame.sprite.Group()
    player1 = Player(cBlue,40,40)
    player1.rect.x = screenX/2
    player1.rect.y = screenY-40
    allSprites.add(player1)

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(cOrange,10,10)
                    bullet.rect.x = player1.rect.x+player1.rect.width/2-bullet.rect.width/2
                    bullet.rect.y = player1.rect.y
                    allSprites.add(bullet)
                    bulletList.add(bullet)
        scr.fill(cBlack)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: player1.rect.x -=3
        if pressed[pygame.K_RIGHT]: player1.rect.x +=3

        allSprites.update()
        for bll in bulletList:
            if bullet.rect.y<-10:
                bulletList.remove(bullet)
                allSprites.remove(bullet)

        allSprites.draw(scr)
        pygame.display.flip()
        clock.tick(60)

main(scrX,scrY)