from torch_ac_agent import NewAgent
import numpy as np
import spike_game
import pygame
import warnings

def nn_learn():
    game = spike_game.mlGame()
    n_games = 2500
    agent = NewAgent(alpha=0.0008, input_dims=[5], gamma=0.97, n_actions=3, l1_size=256, l2_size=256)

    scores=[]

    for i in range(n_games):
        done = False
        score = 0
        observation = game.resetEnv()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = game.getNextFrame(action)
            score += reward
            agent.learn(observation, reward, observation_, done)
            observation=observation_
            game.renderFrame()

        scores.append(score)

        avg_score = np.mean(scores[max(0,i-100):(i+1)])
        print('episode', i, 'score %.2f' % score, 'avg score %.2f' % avg_score)


if __name__ == '__main__':
    #warnings.filterwarnings('ignore')
    nn_learn()
    #autoplay()