import numpy as np
import matplotlib.pyplot as plt
import time

class gridworld(object):
    def __init__(self,m,n,magicSq):
        self.grid = np.zeros((m,n))
        self.m = m
        self.n = n
        self.stateSpace = [i for i in range(self.m*self.n)]
        self.stateSpace.remove(self.m*self.n -1)
        self.stateSpacePlus = [i for i in range(self.m*self.n)]
        self.actionSpace = {'U': -self.m, 'D':self.m, 'L': -1,'R':1}
        self.possibleActions = ['U','D','L','R']
        self.addMagicSq(magicSq)
        self.agentPosition = 0

    def addMagicSq(self, magicSq):
        self.magicSq = magicSq
        i = 2
        for sqr in magicSq:
            x = sqr//self.m
            y = sqr % self.n
            self.grid[x][y]=i
            i+=1
            x = magicSq[sqr]//self.m
            y = magicSq[sqr]%self.n
            self.grid[x][y]=i
            i+=1
    
    def isTerminal(self,state):
        return state in self.stateSpacePlus and state not in self.stateSpace

    def getAgentPos(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.n
        return x,y

    def setSatet(self, state):
        x,y = self.getAgentPos()
        self.grid[x][y] = 0
        self.agentPosition=state
        x,y = self.getAgentPos()
        self.grid[x][y] = 1

    def offGrid(self, newState, oldState):
        if newState not in self.stateSpacePlus:
            return True
        elif oldState % self.m ==0 and newState % self.m == self.m -1:
            return True
        elif oldState % self.m == self.m -1 and newState % self.m ==0:
            return True
        else:
            return False
    
    def step(self, action):
        x,y = self.getAgentPos()
        resState = self.agentPosition + self.actionSpace[action]
        if resState in self.magicSq.keys():
            resState = self.magicSq[resState]

        reward = -1 if not self.isTerminal(resState) else 0
        if not self.offGrid(resState,self.agentPosition):
            self.setSatet(resState)
            return resState,reward,self.isTerminal(self.agentPosition),None
        else:
            return self.agentPosition, reward, self.isTerminal(self.agentPosition),None

    def reset(self):
        self.agentPosition=0
        self.grid = np.zeros((self.m,self.n))
        self.addMagicSq(self.magicSq)
        return self.agentPosition

    def render(self):
        print('-------------------------')
        for row in self.grid:
            for col in row:
                if col == 0:
                    print('-', end = '\t')
                elif col == 1:
                    print('X', end='\t')
                elif col ==2:
                    print('Ain',end='\t')
                elif col == 3:
                    print('Aout',end='\t')
                elif col == 4:
                    print('Bin', end = '\t')
                elif col == 5:
                    print('Bout', end = '\t')
            print('\n')
        print('-------------------------')

    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)
    
def maxAction(Q, state, actions):
    values = np.array([Q[state,a] for a in actions])
    action = np.argmax(values)
    return actions[action]

               
if __name__=='__main__':
    magicSq={10:23}
    env = gridworld(6,6,magicSq)

    ALPHA = 0.1
    GAMMA = 1.0
    EPS = 1.0

    Q = {}
    for state in env.stateSpacePlus:
        for action in env.possibleActions:
            Q[state,action]=0
    
    numGames = 20000
    totalRewords = np.zeros(numGames)
    env.render()

    for i in range(numGames):
        if i % 5000 ==0:
            print('starting game', i)
        done = False
        epRewords = 0
        observation = env.reset()

        while not done:
            rand = np.random.random()
            action = maxAction(Q, observation, env.possibleActions) if rand < (1 - EPS) \
                else env.actionSpaceSample()
            observation_, reward, done, info = env.step(action)
            epRewords +=reward
            action_ = maxAction(Q,observation_,env.possibleActions)
            Q[observation,action]=Q[observation,action] + ALPHA*(reward + \
                GAMMA*Q[observation_,action_] - Q[observation,action])
            observation = observation_
            if i==numGames-1:
                env.render()
                time.sleep(1)
                
        if EPS - 2/ numGames >0:
            EPS -=2/numGames
        else:
            EPS = 0
        totalRewords[i] = epRewords
    plt.plot(totalRewords)
    plt.show()

