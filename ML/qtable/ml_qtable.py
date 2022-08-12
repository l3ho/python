import bomb_game2
import pygame
import numpy as np
import random

def playable():
    clock = pygame.time.Clock()
    game = bomb_game2.mlGame()
    frame = game.resetEnv()
    game.renderFrame()
    done = False
    act = 0
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: act = 2
        if pressed[pygame.K_RIGHT]: act = 1
        if pressed[pygame.K_UP]: act = 4
        if pressed[pygame.K_DOWN]: act = 3
        nframe, score, doneg = game.getNextFrame(act)
        if doneg:
            frame = game.resetEnv()
        game.renderFrame()
        #print(game.bomb_vx,game.bomb_vy)
        act = 0
        clock.tick(60)

def saveQ(Q):
    csvA = []
    for it in Q.items():
        tmps=""
        for kk in range(len(it[0])):
            tmps = tmps + str(it[0][kk]) +","
        tmps = tmps.replace("(","")
        tmps = tmps.replace(")","")
        tmps = tmps.replace(" ","")
        tmps = tmps + str(it[1])            
        csvA.append(tmps)
    with open('ml.txt', 'w') as f:
        for item in csvA:
            f.write("%s\n" % item)

def importQ():
    arr=[]
    Q={}
    with open('ml.txt', 'r') as f:
        for ln in f:
            arr.append(ln.replace("\n",""))
        f.close()
    
    for ii in range(len(arr)):
        splitLine = arr[ii].split(",")
        tmp_state = (int(splitLine[0]),int(splitLine[1]),int(splitLine[2]))
        Q[tmp_state,int(splitLine[3])]=float(splitLine[4])
    return Q

def get_state(frame, player_space, bombx_space, bomby_space):
    plx = frame[1]
    bx = frame[2]
    by = frame[3]
    plx_bin = np.digitize(plx,player_space) 
    bx_bin = np.digitize(bx,bombx_space) 
    by_bin = np.digitize(by,bomby_space)
    return (plx_bin, bx_bin, by_bin)

def max_action(Q,state, actions):
    values = np.array([Q[state,a] for a in actions])
    action = np.argmax(values)
    return action

def learing():
    game = ml_game.mlGame()
    n_games = 8000
    alpha = 0.1
    gamma =0.99
    eps = 1.0
    space_size = 30

    player_space = np.linspace(0, ml_game.winW - ml_game.player_width,space_size)
    bombx_space = np.linspace(0, ml_game.winW-ml_game.bomb_size,space_size)
    bomby_space = np.linspace(0, ml_game.winH-ml_game.bomb_size,space_size)

    states = []
    for pos_x in range(space_size+1):
        for bomb_x in range(space_size+1):
            for bomb_y in range(space_size+1):
                states.append((pos_x,bomb_x,bomb_y))

    Q={}
    for st in states:
        for action in [0,1,2]:
            Q[st,action]=0
    #total_scores = np.zeros(n_games)
    score = 0
    for i in range(n_games):
        done = False
        frm = game.getPresentFrame(False)
        state = get_state(frm,player_space,bombx_space,bomby_space)
        if i%1000==0 and i>0:          
            print('episode',i,'score',score,'epsilon', eps)
            score = 0
        while not done:
            if np.random.random() < eps:
                action = np.random.choice([0,1,2])
            else:
                action = max_action(Q,state,[0,1,2])
            frm_ = game.getNextFrame(action,False)
            done = frm_[4]
            state_ = get_state(frm_,player_space,bombx_space,bomby_space)
            score+=frm_[0]
            action_ = max_action(Q,state_,[0,1,2])
            Q[state,action] = Q[state,action]+alpha*(frm_[0] + \
                gamma*Q[state_,action_] - Q[state,action])
            state = state_
        #total_scores[i] = score
        eps = eps - 2/n_games if eps>0.01 else 0.01
    saveQ(Q)

def autoPlay():
    clock = pygame.time.Clock()
    game = ml_game.mlGame()
    frame = game.getPresentFrame(True)
    space_size = 30
    player_space = np.linspace(0, ml_game.winW - ml_game.player_width,space_size)
    bombx_space = np.linspace(0, ml_game.winW-ml_game.bomb_size,space_size)
    bomby_space = np.linspace(0, ml_game.winH-ml_game.bomb_size,space_size)
    state = get_state(frame,player_space,bombx_space,bomby_space)
    done = False
    scr = 0
    n_scr = 0
    
    Q=importQ()
    action = max_action(Q,state,[0,1,2])
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True

        nframe = game.getNextFrame(action,True)
        state = get_state(nframe,player_space,bombx_space,bomby_space)
        action = max_action(Q,state,[0,1,2,3,4])
        n_scr = game.scount
        if n_scr!=scr:
            print(str(scr))
            scr = n_scr
        if nframe[4]==True:
            done = True
        act = 0
        clock.tick(60)

def main():
    #autoPlay()
    playable()

if __name__ == "__main__":
    main()