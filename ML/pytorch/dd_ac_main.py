from dd_actor_critic import Agent
import numpy as np
import spike_game

agent = Agent(alpha=0.000025, beta=0.00025, input_dims=[5], tau=0.001, env="",
              batch_size=64,  layer1_size=400, layer2_size=300, n_actions=3)

#agent.load_models()
np.random.seed(0)
game = spike_game.mlGame()

score_history = []
for i in range(1000):
    obs = game.resetEnv()
    done = False
    score = 0
    while not done:
        act = agent.choose_action(obs)
        new_state, reward, done = game.getNextFrame(act)
        agent.remember(obs, act, reward, new_state, int(done))
        agent.learn()
        score += reward
        obs = new_state
    score_history.append(score)

    if i % 25 == 0:
        agent.save_models()

    print('episode ', i, 'score %.2f' % score,
          'trailing 100 games avg %.3f' % np.mean(score_history[-100:]))
