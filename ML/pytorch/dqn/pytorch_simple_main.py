from pytorch_nn import Agent
import numpy as np
import pygame
import warnings

def nn_learn():
    game = spike_game.mlGame()
    n_games = 1000
    agent = Agent(gamma=0.99, epsilon=1.0, lr=0.001, input_dims=[3], n_actions=2,
                        mem_size=1000000, batch_size=64, epsilon_end=0.01)

    scores = []
    eps_history = []
    for i in range(n_games):
        done = False
        score = 0
        observation = game.resetEnv()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = game.getNextFrame(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            agent.learn()
            observation = observation_
            game.renderFrame()
        eps_history.append(agent.epsilon)
        scores.append(score)
        avg_score = np.mean(scores[max(0, i-100):(i+1)])
        print('episode', i, 'score %.2f' % score, 'avg score %.2f' % avg_score, 'epsilon %.2f' % agent.epsilon)
    agent.save_models()

def autoplay():
    clock = pygame.time.Clock()
    game = spike_game.mlGame()
    frame = game.resetEnv()
    agent = Agent(gamma=0.99, epsilon=0.0, lr=0.003, input_dims=[2], n_actions=2,
                        mem_size=1000000, batch_size=64, epsilon_end=0.01)
    agent.load_models()
    game.renderFrame()
    done = False
    scr = 0
    n_scr = 0
    observation = game.resetEnv()
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
        action = agent.choose_action(observation)
        observation, score, dead = game.getNextFrame(action)
        game.renderFrame()
        if dead:
            frame = game.resetEnv()
            dead = False
            n_scr = 0    
        n_scr = score
        if n_scr != scr:
            print(str(scr))
            scr = n_scr
        clock.tick(60)

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    nn_learn()
    #autoplay()



