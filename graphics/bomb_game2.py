import pygame 
import numpy as np

winW = 600
winH = 600

bomb_size = 10
bomb_v = 6
player_width = 40
player_height = 40
player_speed = 5
bomb_count = 1

cBlack = (0,0,0)
cWhite = (255,255,255)
cRed = (255,50,50)

pygame.init()
screen = pygame.display.set_mode((winW,winH))
fontx = pygame.font.SysFont("arial", 30)

class bomba():
    def __init__(self,player_x,player_y):
        #self.bomb_x = random.randint(-winW/2+bomb_size*2,winW/2-bomb_size*2)
        #self.bomb_y = int(math.sqrt((winH/2-bomb_size*2)**2-self.bomb_x**2))*random.choice([-1,1])
        self.bomb_x = 0
        self.bomb_y = bomb_size
        self.bomb_vx=bomb_v*(player_x-winW/2 - self.bomb_x)/(winW/2)
        self.bomb_vy=bomb_v*(player_y - self.bomb_y)/(winH/2)
        #self.bomb_vy=bomb_v*(player_y-winW/2 - self.bomb_y)/(winH/2)
        self.bomb_x=self.bomb_x + winH/2 + bomb_size*2
        #self.bomb_y=self.bomb_y + winH/2
    
    def getPos(self):
        return self.bomb_x,self.bomb_y
    def getVelocity(self):
        return self.bomb_vx, self.bomb_vy

    def updatePos(self):
        self.bomb_x += self.bomb_vx
        self.bomb_y += self.bomb_vy
    
    def drawBomb(self):
        bomb=pygame.Rect(self.bomb_x,self.bomb_y,bomb_size,bomb_size)
        pygame.draw.rect(screen,cRed,bomb)    

def drawPlayer(player_x,player_y):
    plr=pygame.Rect(player_x,player_y,player_width,player_height)
    pygame.draw.rect(screen,cWhite,plr)

def collision(bombs,player_x,player_y):
    score = 0
    for i in range(bomb_count):
        bomb_x,bomb_y = bombs[i].getPos()
        bomb_vx,bomb_vy = bombs[i].getVelocity()
        if bomb_y+bomb_size >= player_y and bomb_y <= player_y+player_height and bomb_x + bomb_size>=player_x and bomb_x <=player_x+player_width:
            score = -1
            bombs.remove(bombs[i])
            bombs.append(bomba(player_x,player_y))
            return [bombs,player_x,player_y, True,score]
        if bomb_y +bomb_size>= winH or bomb_y<0 or bomb_x<0 or bomb_x+bomb_size>=winW:
            score = 1
            bombs.remove(bombs[i])
            bombs.append(bomba(player_x,player_y))
            return [bombs,player_x,player_y, False,score]
    return [bombs,player_x,player_y, False,score]

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
        self.bombs = []
        self.done = False

    def resetEnv(self):       
        score = 0
        self.scount = 0
        self.done = False
        self.player_x  = winW/2-player_width/2
        self.player_y =  winH/2-player_height/2
        self.bombs = []
        for i in range(bomb_count):
            self.bombs.append(bomba(self.player_x,self.player_y))

        self.state = []
        self.state.append(self.player_x)
        self.state.append(self.player_y)
        for i in range(bomb_count):
            poss = self.bombs[i].getPos()
            self.state.append(poss[0])
            self.state.append(poss[1])
        return np.array(self.state)

    def getNextFrame(self,action):
        score = 0
        self.player_x, self.player_y = updatePlayer(action,self.player_x, self.player_y)
        for i in range(bomb_count):
            self.bombs[i].updatePos()

        [self.bombs,self.player_x,self.player_y,self.done,score] = collision(self.bombs,self.player_x,self.player_y)

        self.scount = self.scount + score
        if self.scount >=10:
            self.done = True

        self.state = []
        self.state.append(self.player_x)
        self.state.append(self.player_y)
        for i in range(bomb_count):
            poss = self.bombs[i].getPos()
            self.state.append(poss[0])
            self.state.append(poss[1])
 
        return np.array(self.state), score, self.done

    def renderFrame(self):
        pygame.event.pump()  
        screen.fill(cBlack)
        text = fontx.render(str(self.scount), True, (255, 255, 255))
        screen.blit(text,(winW-text.get_width() ,0))
        drawPlayer(self.player_x,self.player_y)
        for i in range(bomb_count):
            self.bombs[i].drawBomb()
        pygame.display.flip()

def playable():
    clock = pygame.time.Clock()
    game = mlGame()
    frame = game.resetEnv()
    game.renderFrame()
    done = False
    act = 0
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: act = 2
        if pressed[pygame.K_RIGHT]: act = 1
        if pressed[pygame.K_UP]: act = 4
        if pressed[pygame.K_DOWN]: act = 3
        nframe, score, doneg = game.getNextFrame(act)
        if doneg:
            frame = game.resetEnv()
        game.renderFrame()
        #print(game.bomb_vx,game.bomb_vy)
        act = 0
        clock.tick(60)    


def main():
    playable()

if __name__ == "__main__":
    main()