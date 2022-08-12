from torch_policy_nn import Agent
import numpy as np
import spike_game
import pygame
import warnings

def nn_learn():
    game = spike_game.mlGame()
    n_games = 2500
    agent = Agent(lr=0.000001, input_dims=[5], gamma=0.99, n_actions=3, l1_size=256, l2_size=256)

    scores=[]

    for i in range(n_games):
        done = False
        score = 0
        observation = game.resetEnv()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = game.getNextFrame(action)
            agent.store_rewards(reward)
            score += reward
            observation=observation_
            game.renderFrame()
        agent.learn()
        scores.append(score)

        avg_score = np.mean(scores[max(0,i-100):(i+1)])
        print('episode', i, 'score %.2f' % score, 'avg score %.2f' % avg_score)


if __name__ == '__main__':
    #warnings.filterwarnings('ignore')
    nn_learn()
    #autoplay()