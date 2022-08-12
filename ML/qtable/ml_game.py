import pygame 
import numpy as np
import random
import math

winW = 600
winH = 600

bomb_size = 10
bomb_v = 4
player_width = 60
player_height = 60
player_speed = 5
bomb_count = 3

cBlack = (0,0,0)
cWhite = (255,255,255)
cRed = (255,50,50)

pygame.init()
screen = pygame.display.set_mode((winW,winH))
fontx = pygame.font.SysFont("arial", 30)

def drawBomb(bomb_x,bomb_y):
    bomb=pygame.Rect(bomb_x,bomb_y,bomb_size,bomb_size)
    pygame.draw.rect(screen,cRed,bomb)

def drawPlayer(player_x,player_y):
    plr=pygame.Rect(player_x,player_y,player_width,player_height)
    pygame.draw.rect(screen,cWhite,plr)

def updateBomb(bomb_x,bomb_y,player_x,player_y, bomb_vx,bomb_vy):
    bomb_y = bomb_y + bomb_vy
    bomb_x = bomb_x + bomb_vx
    score = 0

    if bomb_y+bomb_size >= player_y and bomb_y+bomb_size <= player_y+player_height and bomb_x + bomb_size>=player_x and bomb_x <=player_x+player_width:
        score = -1
        bomb_x,bomb_y,bomb_vy,bomb_vy = resetBomb(player_x,player_y)
        return [score,player_x,player_y,bomb_x,bomb_y, True,bomb_vx,bomb_vy]
    if bomb_y +bomb_size>= winH or bomb_y<0 or bomb_x<0 or bomb_x+bomb_size>=winW:
        score = 1
        bomb_x,bomb_y,bomb_vx,bomb_vy = resetBomb(player_x,player_y)
        return [score,player_x,player_y,bomb_x,bomb_y,False,bomb_vx,bomb_vy]
    return [score,player_x,player_y,bomb_x,bomb_y,False,bomb_vx,bomb_vy]

def resetBomb(player_x,player_y):
    bomb_x = random.randint(-winH/2+bomb_size,winH/2-bomb_size)
    bomb_y = int(math.sqrt((winH/2-bomb_size)**2-bomb_x**2))*random.choice([-1,1])
    bomb_vx=bomb_v*(player_x-winW/2 - bomb_x)/(winW/2)
    bomb_vy=bomb_v*(player_y-winW/2 - bomb_y)/(winH/2)
    bomb_x=bomb_x + winH/2+player_width/2
    bomb_y=bomb_y + winH/2+player_height/2
    print(bomb_vx,bomb_vy)
    return bomb_x,bomb_y, bomb_vx, bomb_vy

def updatePlayer(action,player_x,player_y):
    if action == 1:
        player_x = player_x+player_speed
    elif action == 2:
        player_x = player_x-player_speed
    elif action == 3:
            player_y = player_y+player_speed
    elif action == 4:
        player_y = player_y-player_speed

    if player_x < 0:
        player_x = 0
    elif player_x + player_width > winW:
        player_x = winW - player_width
    elif player_y < 0:
        player_y = 0
    elif player_y + player_height > winH:
        player_y = winH - player_height  
    return player_x, player_y  

class mlGame():
    def __init__(self):
        self.player_x  = winW/2-player_width/2
        self.player_y =  winH/2-player_height/2
        self.scount = 0
        self.bomb_x = self.player_x+player_width/2
        self.bomb_y = bomb_size
        self.done = False
        self.bomb_vx = 0
        self.bomb_vy = 0

    def resetEnv(self):       
        score = 0
        self.scount = 0
        self.done = False
        self.player_x  = winW/2-player_width/2
        self.player_y =  winH/2-player_height/2
        self.bomb_x,self.bomb_y, self.bomb_vx, self.bomb_vy = resetBomb(self.player_x,self.player_y)
        self.state = (self.player_x, self.player_y, self.bomb_x, self.bomb_y)
        return np.array(self.state)

    def getNextFrame(self,action):
        score = 0
        self.player_x, self.player_y = updatePlayer(action,self.player_x, self.player_y)
    
        [score, self.player_x,self.player_y,self.bomb_x,self.bomb_y, self.done, self.bomb_vx, self.bomb_vy] = \
            updateBomb(self.bomb_x,self.bomb_y,self.player_x,self.player_y,self.bomb_vx,self.bomb_vy)

        self.scount = self.scount + score
        if self.scount >=200:
            self.done = True
        self.state = (self.player_x, self.player_y, self.bomb_x, self.bomb_y)
        return np.array(self.state), score, self.done

    def renderFrame(self):
        pygame.event.pump()  
        screen.fill(cBlack)
        text = fontx.render(str(self.scount), True, (255, 255, 255))
        screen.blit(text,(winW-text.get_width() ,0))
        drawPlayer(self.player_x,self.player_y)
        drawBomb(self.bomb_x, self.bomb_y)
        pygame.display.flip()

    