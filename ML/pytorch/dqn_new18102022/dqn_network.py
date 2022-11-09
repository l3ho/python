import torch
import random
from ai_catch_game import mlGame, Point
#from spike_game2 import mlGame
from collections import deque
from dqn_model import Linear_QNet, QTrainer

max_memory = 100_000
batch_size = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=max_memory)
        self.model = Linear_QNet(4, 256, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = [game.catcher.x < game.food.x,
                 game.catcher.x > game.food.x,
                 game.catcher.x < 2,
                 game.catcher.x > game.w - 42]
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > batch_size:
            mini_sample = random.sample(self.memory, batch_size)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 130 - self.n_games
        final_move = [0, 0]
        if random.randint(0, 90) < self.epsilon:
            move = random.randint(0, 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = mlGame()
    game.reset()
    while True:
        # get old state
        state_old = agent.get_state(game)
        # get move
        final_move = agent.get_action(state_old)
        # perform move and get new state
        for ii in range(len(final_move)):
            if final_move[ii] == 1:
                move_int = ii
        reward, done, score = game.play_step(move_int)
        state_new = agent.get_state(game)
        #game.renderFrame()
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()
            if score > record:
                record = score
                print("RECORD SCORE = ", record)
            total_score += score
            mean_score = total_score / agent.n_games
            print('episode', agent.n_games, 'score %.2f' % score, 'avg score %.2f' % mean_score, 'epsilon %.2f' % agent.epsilon)
        if agent.n_games >= 300:
            break


if __name__ == '__main__':
    train()