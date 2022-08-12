import pygame
import numpy as np

cBlack = (0, 0, 0)
cWhite = (255, 255, 255)
cRed = (255, 50, 50)
cGray = (120, 120, 120)
winW = 600
winH = 600
max_moves = 10

pygame.init()
screen = pygame.display.set_mode((winW, winH))
fontX = pygame.font.SysFont("arial", 30)

def draw_player(player_x, player_y, scale_factor):
    tmpRect = pygame.Rect(int((player_x-1) * scale_factor) + 10, int((player_y-1) * scale_factor) + 10, 2 * scale_factor - 20,
                          2 * scale_factor - 20)
    pygame.draw.rect(screen, cRed, tmpRect)

def draw_maze(gArea, scr_size):
    sWidth = scr_size[0]
    sHeight = scr_size[1]
    rectLine = 4
    screen.fill((0, 0, 0))
    for x in range(1, len(gArea[0])-1):
        for y in range(1, len(gArea)-1):
            if gArea[y][x] != 0:
                if x % 2 == 0 and y % 2 != 0:
                    startPoint = (int((x) * sWidth / (len(gArea)-1)), int((y-1) * sHeight / (len(gArea[0])-1)))
                    endPoint = (int((x) * sWidth / (len(gArea)-1)), int((y + 1) * sHeight / (len(gArea[0])-1)))
                    pygame.draw.line(screen, cGray, startPoint, endPoint, rectLine)
                if y % 2 == 0 and x % 2 != 0:
                    startPoint = (int((x-1) * sWidth / (len(gArea)-1)), int((y) * sHeight / (len(gArea[0])-1)))
                    endPoint = (int((x+1) * sWidth / (len(gArea)-1)), int((y) * sHeight / (len(gArea[0])-1)))
                    pygame.draw.line(screen, cGray, startPoint, endPoint, rectLine)
    roomRect = pygame.Rect(0, 0, int(sWidth - rectLine / 2), int(sHeight - 1))
    pygame.draw.rect(screen, cWhite, roomRect, 4)

def collision(player_x, player_y, new_x, new_y, gArea):
    if new_x > 0 and new_x < len(gArea) and new_y > 0 and new_y < len(gArea):
        if player_x != new_x:
            if player_x < new_x: x_pos = player_x - (player_x - new_x)-1
            if player_x > new_x: x_pos = player_x - (player_x - new_x)+1
            wall = gArea[player_y][x_pos]
            if gArea[player_y][x_pos] != 0:
                return True
            else:
                return False
        if player_y != new_y:
            if player_y < new_y: y_pos = player_y - (player_y - new_y)-1
            if player_y > new_y: y_pos = player_y - (player_y - new_y)+1
            wall = gArea[y_pos][player_x]
            if gArea[y_pos][player_x] != 0:
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def update_player(action, player_x, player_y):
    if action == 1:
        #up
        player_y -= 2
    elif action == 2:
        #left
        player_x -= 2
    elif action == 3:
        #down
        player_y += 2
    elif action == 4:
        #right
        player_x += 2
    return player_x, player_y

def check_walls(player_x, player_y, gArea):
    u_wall, l_wall, d_wall, r_wall = 0, 0, 0, 0
    if gArea[player_y + 1][player_x] != 0 or player_y == len(gArea)-1:
        d_wall = 1
    if gArea[player_y - 1][player_x] != 0 or player_y == 0:
        u_wall = 1
    if gArea[player_y][player_x+1] != 0 or player_x == len(gArea)-1:
        r_wall = 1
    if gArea[player_y][player_x-1] != 0 or player_x == 0:
        l_wall = 1
    return u_wall, l_wall, d_wall, r_wall

class mlGame(object):
    def __init__(self):
        self.player_x = 1
        self.player_y = 1
        self.sCount = 0
        self.move_count = 0
        self.done = False
        self.gArea = np.genfromtxt("/python_git/graphics/labirynt.csv", delimiter=';')
        self.player_size = int(winW / (len(self.gArea)-1))

    def resetEnv(self):
        self.sCount = 0
        self.done = False
        self.move_count = 0
        self.player_x = 1
        self.player_y = 1
        u_wall, l_wall, d_wall, r_wall = check_walls(self.player_x, self.player_y, self.gArea)
        return np.array([self.player_x, self.player_y, u_wall, l_wall, d_wall, r_wall], dtype=np.float32)

    def getNextFrame(self, action):
        score = 0
        new_x, new_y = update_player(action, self.player_x, self.player_y)
        col_status = collision(self.player_x, self.player_y, new_x, new_y, self.gArea)

        if col_status:
            score -= 10
        else:
            if self.player_x != new_x or self.player_y != new_y:
                if new_x > self.player_x:
                    score += 5
                if new_y > self.player_y:
                    score += 5
            self.player_x, self.player_y = new_x, new_y
        self.sCount = self.sCount + score
        if new_x == len(self.gArea)-2 and new_y == len(self.gArea)-2:
            self.done = True
            score = 100
        elif self.move_count > max_moves:
            self.done = True
            score = 0
        u_wall, l_wall, d_wall, r_wall = check_walls(self.player_x, self.player_y, self.gArea)
        self.move_count += 1
        return np.array([self.player_x, self.player_y, u_wall, l_wall, d_wall, r_wall], dtype=np.float32), score, self.done

    def renderFrame(self):
        pygame.event.pump()
        screen.fill(cBlack)
        draw_maze(self.gArea, (winW, winH))
        text = fontX.render(str(self.sCount), True, cWhite)
        screen.blit(text, (winW - text.get_width() - 10, 0))
        draw_player(self.player_x, self.player_y, self.player_size)
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP: act = 1
                if event.key == pygame.K_LEFT: act = 2
                if event.key == pygame.K_DOWN: act = 3
                if event.key == pygame.K_RIGHT: act = 4

        nframe, score, doneg = game.getNextFrame(act)
        if doneg:
            done = True
            frame = game.resetEnv()
        game.renderFrame()
        act = 0
        clock.tick(60)

if __name__ == "__main__":
    playable()
