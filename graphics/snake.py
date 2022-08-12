import pygame
from random import randint

scrSize = 600
cBlack = (0,0,0)
cWhite = (255,255,255)
cBlue = (0, 128, 255)
cOrange = (255, 100, 0)

class snakeSegment(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.vx = 0
        self.vy = 0
        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)
        #self.rect = self.image.get_rect()
        self.image = pygame.Surface([width, height],pygame.SRCALPHA)
        rect2 = pygame.Rect(1,1,width-1,height-1)
        rect1 = pygame.Rect(0,0,width,height)
        pygame.draw.rect(self.image,cBlack,rect1)
        pygame.draw.rect(self.image,color,rect2)
        self.rect = self.image.get_rect() 

class snakeFood(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

def randomizeFood(sSize):
    sf = snakeFood(cOrange,sSize,sSize)
    sf.rect.x = randint(2,(scrSize-sSize)/sSize)*sSize
    sf.rect.y = randint(2,(scrSize-sSize)/sSize)*sSize
    return sf

def snakeAdd(seg,segSize):
    stmp=snakeSegment(cBlue,segSize,segSize)
    if seg[len(seg)-1].vx == 1:
        stmp.rect.x = seg[len(seg)-1].rect.x-segSize
        stmp.rect.y = seg[len(seg)-1].rect.y
    elif seg[len(seg)-1].vx == -1:
        stmp.rect.x = seg[len(seg)-1].rect.x+segSize
        stmp.rect.y = seg[len(seg)-1].rect.y
    elif seg[len(seg)-1].vy == 1:
        stmp.rect.x = seg[len(seg)-1].rect.x
        stmp.rect.y = seg[len(seg)-1].rect.y-segSize
    elif seg[len(seg)-1].vy == -1:
        stmp.rect.x = seg[len(seg)-1].rect.x
        stmp.rect.y = seg[len(seg)-1].rect.y+segSize

    return stmp

def moveSnake(sAr,sSize):
    for i in range(len(sAr),0,-1):
        if i>0 and i<len(sAr):
            sAr[i].vx = sAr[i-1].vx
            sAr[i].vy = sAr[i-1].vy
            sAr[i].rect.x = sAr[i-1].rect.x
            sAr[i].rect.y = sAr[i-1].rect.y
    sAr[0].rect.x = sAr[0].rect.x + sAr[0].vx*sSize
    sAr[0].rect.y = sAr[0].rect.y + sAr[0].vy*sSize

def main():
    segSize = 20
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((scrSize, scrSize))
    fontx = pygame.font.SysFont("comicsansms", 20)
    done = False

    allSprites = pygame.sprite.Group()
    segments = pygame.sprite.Group()
    segArr=[]
    
    player1 = snakeSegment(cWhite,segSize,segSize)
    player1.rect.x = scrSize/2
    player1.rect.y = scrSize/2
    food1 = randomizeFood(segSize)
    segArr.append(player1)
    allSprites.add(player1)
    allSprites.add(food1)

    score = 0

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: 
                    player1.vx =-1
                    player1.vy = 0
                if event.key == pygame.K_RIGHT: 
                    player1.vx =1
                    player1.vy = 0
                if event.key == pygame.K_UP: 
                    player1.vy =-1
                    player1.vx = 0
                if event.key == pygame.K_DOWN: 
                    player1.vy = 1
                    player1.vx = 0

        scr.fill(cBlack)
        moveSnake(segArr,segSize)
        allSprites.update()

        if scr.get_rect().contains(player1)==False:
            done = True

        if pygame.sprite.collide_rect(player1,food1):
            score+=1
            sg = snakeAdd(segArr,segSize)
            allSprites.add(sg) 
            segArr.append(sg)
            segments.add(sg)
            allSprites.remove(food1)
            food1 = randomizeFood(segSize)
            allSprites.add(food1)   
       
        block_hit_list = pygame.sprite.spritecollide(player1, segments, True)

        for bl in block_hit_list:
            text = fontx.render("GAME OVER", True, (255, 255, 255))
            scr.blit(text,(scrSize/2-text.get_width() ,0))
            done = True

        text = fontx.render(str(score), True, (255, 255, 255))
        scr.blit(text,(scrSize-text.get_width() ,0))
        allSprites.draw(scr)
        pygame.display.flip()
        clock.tick(8)

main()
