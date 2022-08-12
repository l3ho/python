from ml_keras1 import Agent
from keras.models import load_model
import numpy as np
import spike_game
import pygame
from keras.backend import manual_variable_initialization

def nn_learn():
    game = spike_game.mlGame()
    n_games = 1000
    agent = Agent(gamma=0.95,epsilon = 1.0, alpha = 0.00005, input_dims=5,n_actions=3,
    mem_size = 1000000,batch_size = 64, epsilon_end =0.01)

    scores=[]
    eps_history = []
    manual_variable_initialization(True)
    for i in range(n_games):
        done = False
        score = 0
        observation = game.resetEnv()

        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = game.getNextFrame(action)
            score +=reward
            agent.remember(observation,action,reward,observation_,done)
            observation=observation_
            agent.learn()
            game.renderFrame()

        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[max(0,i-100):(i+1)])
        print('episode', i, 'score %.2f' % score, 'avg score %.2f' % avg_score, 'epsilon %.2f' % agent.epsilon)

        if i%10 == 0 and i>0:
            agent.save_model()
            print('saving')

def autoplay():
    clock = pygame.time.Clock()
    game = spike_game.mlGame()
    frame = game.resetEnv()

    #agent = Agent(gamma=0.99,epsilon = 0.0, alpha = 0.0005, input_dims=3,n_actions=3,
    #mem_size = 1000000,batch_size = 64, epsilon_end =0.01)

    agent = load_model('dqn_model.h5')

    game.renderFrame()
    done = False
    scr = 0
    n_scr = 0

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
        frame = frame[np.newaxis,:]
        actions = agent.predict(frame)
        action = np.argmax(actions)
        frame, score, dead = game.getNextFrame(action)     
        game.renderFrame()
        if dead:
            frame = game.resetEnv()
            dead = False
            n_scr = 0    
        n_scr = game.scount
        if n_scr!=scr:
            print(str(scr))
            scr = n_scr
        clock.tick(100)    


if __name__ == '__main__':
    nn_learn()
    #autoplay()



