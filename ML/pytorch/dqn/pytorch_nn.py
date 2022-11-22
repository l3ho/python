import numpy as np
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class dqnetwork(nn.Module):
    def __init__(self, lr, input_dims, fc1_dims, fc2_dims, n_actions):
        super(dqnetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = T.device('cuda' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        #state = T.Tensor(observation).to(self.device)
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)
        return actions

    def save_checkpoint(self):
        print('... saving checkpoint ...')
        T.save(self.state_dict(), 'dqn_model.pt')

    def load_checkpoint(self):
        print('... loading checkpoint ...')
        self.load_state_dict(T.load('dqn_model.pt'))

class Agent(object):
    def __init__(self, gamma, epsilon, lr, batch_size, input_dims, n_actions, epsilon_dec=1e-5,
                    epsilon_end=0.01, mem_size=1000000):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.mem_size = mem_size
        self.mem_cntr = 0
        self.q_eval = dqnetwork(lr, n_actions=n_actions, input_dims=input_dims, fc1_dims=256, fc2_dims=256)
        #self.q_next = dqnetwork(lr, n_actions=n_actions, input_dims=input_dims, fc1_dims=64, fc2_dims=64)
        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done
        self.action_memory[index] = action
        self.mem_cntr += 1

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = T.tensor([observation]).to(self.q_eval.device)
            actions = self.q_eval.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)
        return action

    def learn(self):
        if self.mem_cntr > self.batch_size:
            self.q_eval.optimizer.zero_grad()
            max_mem = min(self.mem_cntr, self.mem_size)
            batch = np.random.choice(max_mem, self.batch_size, replace=False)
            batch_index = np.arange(self.batch_size, dtype=np.int32)

            state_batch = T.tensor(self.state_memory[batch]).to(self.q_eval.device)
            new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.q_eval.device)
            reward_batch = T.tensor(self.reward_memory[batch]).to(self.q_eval.device)
            terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.q_eval.device)
            action_batch = self.action_memory[batch]

            q_eval = self.q_eval.forward(state_batch)[batch_index, action_batch]
            q_next = self.q_eval.forward(new_state_batch)
            q_next[terminal_batch] = 0.0

            q_target = reward_batch + self.gamma*T.max(q_next, dim=1)[0]
            loss = self.q_eval.loss(q_target, q_eval).to(self.q_eval.device)
            loss.backward()
            self.q_eval.optimizer.step()

            self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > self.epsilon_min else self.epsilon_min

    def save_models(self):
        self.q_eval.save_checkpoint()

    def load_models(self):
        self.q_eval.load_checkpoint()







