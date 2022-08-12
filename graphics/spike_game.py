import pygame
import numpy as np

winW = 600
winH = 300
border = 50

spike_w = 30
spike_v = -6
player_width = 30
player_height = 80
player_v = -10
spike_count = 1

cBlack = (0, 0, 0)
cWhite = (255, 255, 255)
cRed = (255, 50, 50)
cGray = (120, 120, 120)

pygame.init()
screen = pygame.display.set_mode((winW, winH))
fontX = pygame.font.SysFont("arial", 30)


class Spike(object):
    def __init__(self):
        self.spike_x = winW - spike_w
        spike_type = np.random.choice((2, 2))
        if spike_type == 1:
            self.spike_h = 150
            self.spike_y = border
        elif spike_type == 2:
            self.spike_h = 50
            self.spike_y = winH - border - self.spike_h
        self.spike_v = spike_v

    def get_pos(self):
        return self.spike_x, self.spike_y, self.spike_h

    def update_pos(self):
        self.spike_x += self.spike_v

    def draw_spike(self):
        spike_rect = pygame.Rect(self.spike_x, self.spike_y, spike_w, self.spike_h)
        pygame.draw.rect(screen, cRed, spike_rect)


def draw_player(player_x, player_y, player_h):
    plr = pygame.Rect(player_x, player_y, player_width, player_h)
    pygame.draw.rect(screen, cWhite, plr)


def draw_boarders():
    b1 = pygame.Rect(0, 0, winW, border)
    pygame.draw.rect(screen, cGray, b1)
    b2 = pygame.Rect(0, winH - border, winW, border)
    pygame.draw.rect(screen, cGray, b2)


def collision(spikes, player_x, player_y, player_h):
    score = 0
    for i in range(spike_count):
        spike_x, spike_y, spike_h = spikes[i].get_pos()

        if spike_y + spike_h >= player_y and spike_y <= player_y + player_h and spike_x + spike_w >= player_x and \
                spike_x <= player_x + player_width:
            score = 0
            spikes.remove(spikes[i])
            spikes.append(Spike())
            return [spikes, True, score]
        if spike_x <= 0:
            score = 10
            spikes.remove(spikes[i])
            spikes.append(Spike())
            return [spikes, False, score]
    return [spikes, False, score]


def player_jump(player_y, jump_v):
    player_y = player_y + jump_v
    if player_y <= border:
        jump_v = 3
    if player_y >= winH - player_height - border:
        jump_v = player_v
        return player_y, False, jump_v

    else:
        return player_y, True, jump_v


def update_player(action, player_y, jump_flag):
    if action == 1:
        jump_flag = True
        player_h = player_height
    elif action == 2:
        player_y = winH - player_height / 2 - border
        player_h = player_height / 2
    else:
        player_h = player_height
        player_y = winH - player_height - border
    return player_y, player_h, jump_flag


class mlGame(object):
    def __init__(self):
        self.player_x = 0
        self.player_y = 0
        self.player_h = player_height
        self.sCount = 0
        self.spikes = []
        self.done = False
        self.jump_flag = False
        self.jump_v = player_v

    def resetEnv(self):
        self.sCount = 0
        self.done = False
        self.player_x = winW / 4
        self.player_y = winH - player_height - border
        self.spikes = []
        for i in range(spike_count):
            self.spikes.append(Spike())

        #img_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #return img_data
        self.state = []
        self.state.append(self.player_x)
        self.state.append(self.player_y)
        for i in range(spike_count):
            poss = self.spikes[i].get_pos()
            self.state.append(poss[0])
            self.state.append(poss[1])
            #self.state.append(poss[2])
        return np.array(self.state)

    def getNextFrame(self, action):
        score = 0
        player_h = player_height

        if self.jump_flag is False:
            self.player_y, self.player_h, self.jump_flag = update_player(action, self.player_y, self.jump_flag)
        else:
            self.player_y, self.jump_flag, self.jump_v = player_jump(self.player_y, self.jump_v)
        for i in range(spike_count):
            self.spikes[i].update_pos()

        [self.spikes, self.done, score] = collision(self.spikes, self.player_x, self.player_y, self.player_h)

        self.sCount = self.sCount + score
        if self.sCount >= 10:
            self.done = True
            score = 100
        elif self.done == True and self.sCount <10:
            score = -100

        #img_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #return img_data, score, self.done
        self.state = []
        self.state.append(self.player_x)
        self.state.append(self.player_y)
        for i in range(spike_count):
            poss = self.spikes[i].get_pos()
            self.state.append(poss[0])
            self.state.append(poss[1])
            #self.state.append(poss[2])
        return np.array(self.state), score, self.done

    def renderFrame(self):
        pygame.event.pump()
        screen.fill(cBlack)
        draw_boarders()
        text = fontX.render(str(self.sCount), True, cBlack)
        screen.blit(text, (winW - text.get_width(), 0))
        draw_player(self.player_x, self.player_y, self.player_h)
        for i in range(spike_count):
            self.spikes[i].draw_spike()
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
        if pressed[pygame.K_DOWN]: act = 2
        if pressed[pygame.K_UP]: act = 1

        nframe, score, doneg = game.getNextFrame(act)
        if doneg:
            frame = game.resetEnv()
        game.renderFrame()
        act = 0
        clock.tick(60)


if __name__ == "__main__":
    playable()
