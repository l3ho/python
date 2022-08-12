import pygame
import numpy as np
import random
import math
import time

white = (255, 255, 255)
gray = (70, 70, 70)
dark_gray = (10, 10, 10)
green = (0, 200, 0)
blue = (0, 0, 200)
cBlack = (0, 0, 0)

sol_list = []
shortest_ln = -1


def gen_maze(empty_maze, maze_dens):
    for i in range(len(empty_maze[0])):
        for j in range(len(empty_maze)):
            if (i % 2 != 0 and j % 2 == 0) or (j % 2 != 0 and i % 2 == 0):
                empty_maze[i][j] = random.randint(0, maze_dens)
                #empty_maze[i][j] = 1
            if i == 0 or j == 0 or i == len(empty_maze[0])-1 or j == len(empty_maze)-1:
                empty_maze[i][j] = 1
    return empty_maze


def randomizePath(gArea, pointCount):
    maxX = len(gArea) - 1
    maxY = len(gArea[0]) - 1
    pathPoints = np.zeros((pointCount, 3))
    fullPath = []
    for i in range(pointCount):
        if i > 0 and i < pointCount - 1:
            pathPoints[i][0] = random.randrange(1, len(gArea) - 1, 2)
            pathPoints[i][1] = random.randrange(1, len(gArea) - 1, 2)
        elif i == pointCount - 1:
            pathPoints[i][0] = maxX - 1
            pathPoints[i][1] = maxY - 1
        elif i == 0:
            pathPoints[i][0] = 1
            pathPoints[i][1] = 1
        pathPoints[i][2] = math.sqrt((1 - pathPoints[i][1]) ** 2 + (1 - pathPoints[i][0]) ** 2)

    ind = np.argsort(pathPoints[:, -1])
    pathPoints = pathPoints[ind]
    for i in range(pointCount):
        fullPath.append((int(pathPoints[i][0]), int(pathPoints[i][1]), "point"))
    s_pos_x = 1
    s_pos_y = 1
    for i in range(pointCount):
        for y in range(abs(int(pathPoints[i][1] - s_pos_y))):
            if s_pos_y <= int(pathPoints[i][1]):
                iterator = s_pos_y + y
            else:
                iterator = s_pos_y - y
            if gArea[int(iterator)][int(s_pos_x)] != 0: gArea[int(iterator)][int(s_pos_x)] = 0
            if iterator % 2 != 0:
                if (int(s_pos_x), int(iterator), "point") not in fullPath:
                    fullPath.append((int(s_pos_x), int(iterator), "path"))
        for x in range(abs(int(pathPoints[i][0] - s_pos_x))):
            if s_pos_x <= int(pathPoints[i][0]):
                iterator = s_pos_x + x
            else:
                iterator = s_pos_x - x
            if gArea[int(pathPoints[i][1])][int(iterator)] != 0: gArea[int(pathPoints[i][1])][int(iterator)] = 0
            if iterator % 2 != 0:
                if (int(iterator), int(pathPoints[i][1]), "point") not in fullPath:
                    fullPath.append((int(iterator), int(pathPoints[i][1]), "path"))
        s_pos_x = pathPoints[i][0]
        s_pos_y = pathPoints[i][1]
    return gArea, fullPath


def drawArea(screen, gArea, mPath, scr_size):
    sWidth = scr_size[0]
    sHeight = scr_size[1]
    rectLine = 4
    screen.fill((0, 0, 0))
    for x in range(1, len(gArea[0])-1):
        for y in range(1, len(gArea)-1):
            if gArea[y][x] != 0:
                if x % 2 == 0 and y % 2 != 0:
                    startPoint = (int((x) * sWidth / (len(gArea)-1)), int((y-1) * sHeight / (len(gArea[0])-1)))
                    endPoint = (int((x) * sWidth / (len(gArea)-1)), int((y + 1) * sHeight / (len(gArea[0])-1)))
                    pygame.draw.line(screen, gray, startPoint, endPoint, rectLine)
                if y % 2 == 0 and x % 2 != 0:
                    startPoint = (int((x-1) * sWidth / (len(gArea)-1)), int((y) * sHeight / (len(gArea[0])-1)))
                    endPoint = (int((x+1) * sWidth / (len(gArea)-1)), int((y) * sHeight / (len(gArea[0])-1)))
                    pygame.draw.line(screen, gray, startPoint, endPoint, rectLine)
    sq_size = 20
    for i in range(len(mPath)):
        tmpRect = pygame.Rect(int((mPath[i][0]-1) * sWidth / (len(gArea)-1)) + sq_size, int((mPath[i][1]-1) * sHeight / (len(gArea)-1))
                              + sq_size, 2 * int(sWidth / (len(gArea)-1)) - 2*sq_size, 2 * int(sWidth / (len(gArea)-1)) - 2*sq_size)
        pygame.draw.rect(screen, green, tmpRect)

    roomRect = pygame.Rect(0, 0, int(sWidth - rectLine / 2),
                           int(sHeight - 1))
    pygame.draw.rect(screen, white, roomRect, 4)
    pygame.display.flip()


def check_move(pos_xy, move_n, game_area):
    new_pos_xy = pos_xy
    if move_n == 1:
        # up
        if 0 < pos_xy[1] < len(game_area) - 2:
            if game_area[pos_xy[1] - 1][pos_xy[0]] == 0:
                new_pos_xy = (pos_xy[0], pos_xy[1] - 2)
    elif move_n == 2:
        # left
        if 0 < pos_xy[0] < len(game_area) - 2:
            if game_area[pos_xy[1]][pos_xy[0] - 1] == 0:
                new_pos_xy = (pos_xy[0] - 2, pos_xy[1])
    elif move_n == 3:
        # down
        if 0 <= pos_xy[1] < len(game_area) - 2:
            if game_area[pos_xy[1] + 1][pos_xy[0]] == 0:
                new_pos_xy = (pos_xy[0], pos_xy[1] + 2)
    elif move_n == 4:
        # right
        if 0 <= pos_xy[0] < len(game_area) - 2:
            if game_area[pos_xy[1]][pos_xy[0] + 1] == 0:
                new_pos_xy = (pos_xy[0] + 2, pos_xy[1])
    return new_pos_xy


def nextMove(current_sol, game_area, nn):
    global shortest_ln
    if current_sol[len(current_sol) - 1] == (len(game_area) - 2, len(game_area) - 2):
        if shortest_ln == -1 or shortest_ln > len(current_sol):
            sol_list.append(current_sol.copy())
            shortest_ln = len(current_sol)
    else:
        pos_xy = current_sol[len(current_sol) - 1]
        for i in range(1, 5):
            new_pos = check_move(pos_xy, i, game_area)
            if new_pos != pos_xy and new_pos not in current_sol and (
                    len(current_sol) + 1 < shortest_ln or shortest_ln == -1):
                current_sol.append(new_pos)
                nextMove(current_sol, game_area, nn + 1)
                current_sol.remove(new_pos)


def calc_rec_path(g_area):
    start_rec = time.time()
    global shortest_ln
    shortest_ln = -1
    current_sol = []
    nn = 0
    current_sol.append((1, 1))
    nextMove(current_sol, g_area, nn)
    shortest_paths = []
    # find shortest path (or paths)
    nn = -1
    for i in range(len(sol_list)):
        if nn == -1 or nn > len(sol_list[i]):
            nn = len(sol_list[i])
    for i in range(len(sol_list)):
        if len(sol_list[i]) == nn:
            shortest_paths.append(sol_list[i])

    return shortest_paths[0], format((time.time() - start_rec), ".2f")


def create_full_graph(g_area):
    vertices = int(((len(g_area)-1)/2))**2 + 1
    v_matrix = np.zeros((vertices, vertices), dtype='uint8')
    cntr = 1
    for y in range(1, len(g_area)-1, 2):
        for x in range(1, len(g_area)-1, 2):
            if x > 1 and y > 1:
                v_pos = int((y+1)/2) + int(((len(g_area)-1)/2)*((x-1)/2))
            elif x == 1 and y > 1:
                v_pos = int((y+1)/2)
            elif x == 1 and y == 1:
                v_pos = 1
            else:
                v_pos = int(((len(g_area)-1)/2)*((x-1)/2))+1
            #print(y, x, v_pos)
            #up
            if y > 1:
                if g_area[y-1][x] == 0:
                    v_matrix[v_pos][v_pos - 1] = 1
            #left
            if x > 1:
                if g_area[y][x-1] == 0:
                    v_matrix[v_pos][v_pos - int((len(g_area)-1)/2)] = 1
            #down
            if y < len(g_area)-1:
                if g_area[y+1][x] == 0:
                    if v_pos+1 < vertices:
                        v_matrix[v_pos][v_pos + 1] = 1
            #right
            if x < len(g_area)-1:
                if g_area[y][x+1] == 0:
                    if v_pos + int((len(g_area)-1)/2) < vertices:
                        v_matrix[v_pos][v_pos + int((len(g_area)-1)/2)] = 1
        cntr += 1
    return v_matrix


def bfs_algorithm(v_matrix):
    visited = np.zeros((len(v_matrix), 2), dtype='uint16')
    v_queue = []
    v_queue.append((1, 1))
    current_dsist = 0
    level_switch = False
    while len(v_queue) > 0:
        node = v_queue[0]
        if node[0] > 0:
            visited[node[0]] = (node[1], visited[node[1]][1]+1)
        else:
            visited[node[0]] = (node[1], 1)
        v_queue.remove((node[0], node[1]))
        if node[0] == len(v_matrix)-1:
            break
        for i in range(1, len(v_matrix)):
            if v_matrix[node[0]][i] != 0:
                if visited[i][1] == 0:
                    v_queue.append((i, node[0]))
    return visited


def calc_bfs_path(g_area):
    start_rec = time.time()
    ver_matrix = create_full_graph(g_area)
    vis_table = bfs_algorithm(ver_matrix)
    node_path = []
    last_node = False
    next_node = len(vis_table)-1
    node_path.append((len(g_area) - 2, len(g_area) - 2))
    #print(vis_table[len(vis_table)-1][1])
    while next_node != 1:
        next_node = vis_table[next_node][0]
        #node to points
        point_y = math.floor((next_node-1)/((len(g_area)-1)/2))*2 + 1
        point_x = ((next_node-1) % ((len(g_area)-1)/2))*2 + 1
        print(next_node, point_x, point_y)
        node_path.append((int(point_y), int(point_x)))
    return node_path, format((time.time() - start_rec), ".2f")


def create_simplified_graph(g_area):
    node_list = []
    visited_list = []
    node_list.append((1, 1))
    visited_list.append((1, 1))
    for y in range(1, len(g_area)-1, 2):
        for x in range(1, len(g_area)-1, 2):
            if g_area[y][x] == 0 and (x, y) not in visited_list:
                #move up
                yy = y
                xx = x
                if g_area[y-1][x] == 0:
                    while g_area[yy][xx] == 0:
                        if g_area[yy][xx] == 0 and (xx, yy) not in visited_list:
                            visited_list.append((xx, yy))
                            if check_if_node(xx, yy, g_area):
                                node_list.append((xx, yy))
                        if g_area[yy - 1][xx] != 0: break
                        yy = yy - 2
                #move down
                yy = y
                xx = x
                if g_area[y+1][x] == 0:
                    while g_area[yy][xx] == 0:
                        if g_area[yy][xx] == 0 and (xx, yy) not in visited_list:
                            visited_list.append((xx, yy))
                            if check_if_node(xx, yy, g_area):
                                node_list.append((xx, yy))
                        if g_area[yy + 1][xx] != 0: break
                        yy = yy + 2
                #move left
                yy = y
                xx = x
                if g_area[y][x-1] == 0:
                    while g_area[yy][xx] == 0:
                        if g_area[yy][xx] == 0 and (xx, yy) not in visited_list:
                            visited_list.append((xx, yy))
                            if check_if_node(xx, yy, g_area):
                                node_list.append((xx, yy))
                        if g_area[yy][xx-1] != 0: break
                        xx = xx - 2
                #move right
                yy = y
                xx = x
                if g_area[y][x+1] == 0:
                    while g_area[yy][xx] == 0:
                        if g_area[yy][xx] == 0 and (xx, yy) not in visited_list:
                            visited_list.append((xx, yy))
                            if check_if_node(xx, yy, g_area):
                                node_list.append((xx, yy))
                        if g_area[yy][xx+1] != 0: break
                        xx = xx + 2
    return node_list

def check_if_node(pos_x, pos_y, g_area):
    is_node = True
    if pos_x == 1 and pos_y == 5:
        ble =1
    if g_area[pos_y-1][pos_x] == 0 and g_area[pos_y+1][pos_x] == 0 and (g_area[pos_y][pos_x-1] != 0 and g_area[pos_y][pos_x+1] != 0):
        is_node = False
    if g_area[pos_y][pos_x-1] == 0 and g_area[pos_y][pos_x+1] == 0 and (g_area[pos_y-1][pos_x] != 0 and g_area[pos_y+1][pos_x] != 0):
        is_node = False
    return is_node

def main():
    pygame.init()
    clock = pygame.time.Clock()
    random.seed(14)
    areaWidth = 5
    areaHeight = 5
    screenSize = (600, 600)
    maze_density = 2
    maze_points = 3
    gameArea = np.zeros((areaWidth * 2 + 1, areaHeight * 2 + 1), dtype='uint8')
    scr = pygame.display.set_mode(screenSize)
    mazePath = []
    gameArea = gen_maze(gameArea, maze_density)
    #drawArea(scr, gameArea, mazePath, screenSize)
    gameArea, mazePatha = randomizePath(gameArea, maze_points)
    drawArea(scr, gameArea, mazePath, screenSize)
    np.savetxt("labirynt.csv", gameArea, delimiter=";")
    #maze_path = create_simplified_graph(gameArea)
    # recursive
    #maze_path, rec_time = calc_rec_path(gameArea)
    #print("Recursive path : time {0}s, length {1}".format(rec_time, len(maze_path)))
    #graphs
    #maze_path, rec_time = calc_bfs_path(gameArea)
    #print("BFS path : time {0}s, length {1}".format(rec_time, len(maze_path)))
    #print(maze_path)
    #drawArea(scr, gameArea, maze_path, screenSize)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(60)


main()
# np.savetxt("labirynt.csv", gameArea, delimiter=";")
# gameArea = np.genfromtxt("labirynt.csv", delimiter=';')