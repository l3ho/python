import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 100
Point = namedtuple('Point', 'x, y')


class mlGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Catcher')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.catcher = Point(self.w / 2, self.h - BLOCK_SIZE)
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = 0
        self.food = Point(x, y)

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # 2. move
        self._move_food()
        self._move(action)  # update the head
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.is_collision(self.food):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        # 4. place new food or just move
        if (self.food.x + BLOCK_SIZE > self.catcher.x and self.food.x < self.catcher.x + BLOCK_SIZE*2) and (self.food.y > self.h - BLOCK_SIZE*2 and self.food.y < self.h):
            self.score += 1
            reward = 10
            self._place_food()
        if self.score == 20:
            reward = 100
            game_over = True
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.catcher
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE * 2 or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        return False

    def renderFrame(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(self.catcher.x, self.catcher.y, BLOCK_SIZE*2, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(self.catcher.x + 4, self.catcher.y + 4, 32, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        self.clock.tick(SPEED)

    def _move(self, action):
        x = self.catcher.x
        y = self.catcher.y
        if action == 0:
            x += BLOCK_SIZE
        elif action == 1:
            x -= BLOCK_SIZE
        self.catcher = Point(x, y)

    def _move_food(self):
        x = self.food.x
        y = self.food.y
        y += BLOCK_SIZE/2
        self.food = Point(x, y)

def playable():
    clock = pygame.time.Clock()
    game = mlGame()
    frame = game.reset()
    game._update_ui()
    done = False
    act = -1
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: act = 1
        if pressed[pygame.K_RIGHT]: act = 0
        reward, doneg, score = game.play_step(act)
        if doneg:
            frame = game.reset()
        game.renderFrame()
        #print(game.bomb_vx,game.bomb_vy)
        act = -1
        clock.tick(60)

def main():
    playable()

if __name__ == "__main__":
    main()