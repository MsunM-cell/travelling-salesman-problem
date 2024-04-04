from cmath import log
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import math


# 读取城市的x，y坐标
def load(txt):
    f = open(txt)
    map = []
    flag = 0
    for line in f:
        line = line.strip()
        if line == "NODE_COORD_SECTION":
            flag = 1
            continue
        if line == "EOF":
            break
        if flag:
            a = line.split()
            map.append((float(a[1]), float(a[2])))
    return tuple(map)


# 获取两个城市间的二维欧几里得距离
def getDist():
    global map, size
    dist = np.zeros((size, size))
    for i in range(0, size):
        for j in range(0, size):
            dist[i][j] = ((map[i][0] - map[j][0]) ** 2 + (map[i][1] - map[j][1]) ** 2) ** 0.5
    return dist


txt = "rd100.tsp"
map = load(txt)
size = len(map)
visited = {}
solutions = []
DIST = getDist()
count = 0


# 根据路径获取该路径总代价
def getCost(path):
    cost = 0
    former = path[0]
    for city in path:
        cost += DIST[former][city]
        former = city
    cost += DIST[path[0]][path[-1]]
    return cost


# 扰动产生新的随机解，扰动方式为分成四个区间随机排序
def shaking(path):
    global size
    ini = visited[path]
    cnt = 0
    while True:
        pos1, pos2, pos3 = sorted(random.sample(range(0, size), 3))
        path_ = path[pos1:pos2] + path[:pos1] + path[pos3:] + path[pos2:pos3]
        if path_ not in visited:
            cost = getCost(path_)
            visited.update({path_: cost})
        else:
            cost = visited[path_]
        cnt += 1
        if ini >= cost:
            break
        elif cnt > 100:
            path_ = path
            cost = ini
            break
    return path_


# 反转一段区间，获取新邻域
def getNei_rev(path):
    global size
    min = 1000000000
    for cnt in range(100):
        i, j = sorted(random.sample(range(1, size - 1), 2))
        path_ = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
        if path_ not in visited:
            cost = getCost(path_)
            visited.update({path_: cost})
        else:
            cost = visited[path_]
        if cost < visited[path]:
            min = cost
            p = path_
            break
        if cost < min:
            min = cost
            p = path_
        '''cost -= DIST[path[i]][path[i-1]] + DIST[path[j]][path[j+1]]
        cost += DIST[path[i-1]][path[j]] + DIST[path[i]][path[j+1]]
        if int(cost) == int(getCost(path_)):
            break
        else:
            continue'''
    return p, min


# 交换两个城市，获取新邻域
def getNei_exc(path):
    global size
    min = 1000000000
    for cnt in range(100):
        i, j = sorted(random.sample(range(1, size - 1), 2))
        path_ = path[:i] + path[j:j + 1] + path[i + 1:j] + path[i:i + 1] + path[j + 1:]
        if path_ not in visited:
            cost = getCost(path_)
            visited.update({path_: cost})
        else:
            cost = visited[path_]
        if cost < visited[path]:
            min = cost
            p = path_
            break
        if cost < min:
            min = cost
            p = path_
        '''cost -= DIST[path[i]][path[i-1]] + DIST[path[j]][path[j-1]] + DIST[path[i]][path[i+1]] + DIST[path[j]][path[j+1]]
        cost += DIST[path[i-1]][path[j]] + DIST[path[j]][path[i+1]] + DIST[path[j-1]][path[i]] + DIST[path[i]][path[j+1]]
        if int(cost) == int(getCost(path_)):
            break
        else:
            continue'''
    return p, min


# 随机挑选两个城市插入序列头部，获取新邻域
def getNei_ins(path):
    global size
    min = 1000000000
    for cnt in range(100):
        i, j = sorted(random.sample(range(1, size - 1), 2))
        path_ = path[i:i + 1] + path[j:j + 1] + path[:i] + path[i + 1:j] + path[j + 1:]
        if path_ not in visited:
            cost = getCost(path_)
            visited.update({path_: cost})
        else:
            cost = visited[path_]
        if cost < visited[path]:
            min = cost
            p = path_
            break
        if cost < min:
            min = cost
            p = path_
        '''cost -= DIST[path[i]][path[i-1]] + DIST[path[j]][path[j-1]] + DIST[path[i]][path[i+1]] + DIST[path[j]][path[j+1]] + DIST[path[0]][path[-1]]
        cost += DIST[path[i]][path[j]] + DIST[path[j]][path[0]] + DIST[path[i-1]][path[i+1]] + DIST[path[j-1]][path[j+1]] + DIST[path[-1]][path[i]]
        if int(cost) == int(getCost(path_)):
            break
        else:
            continue'''
    return p, min


# 在Local Search中使用VND方法进行搜索
def VND(path):
    path, min = getNei_rev(path)
    l = 1
    while l < 3:
        if l == 0:
            path_, cost = getNei_rev(path)
        elif l == 1:
            path_, cost = getNei_exc(path)
        elif l == 2:
            path_, cost = getNei_ins(path)
        if cost < min:
            path = path_
            min = cost
            l = 0
        else:
            l += 1
    return path, min


# 模拟退火算法
def SA(path, kmax, t0, t_end):
    temp = path
    min = solutions[0]
    result = [temp, min]  # 记录迭代过的最优的解
    global count
    t = t0  # 初始温度
    while t > t_end:
        for k in range(1, kmax):
            path_nei, cost = VND(shaking(temp))  # 进行变邻域操作
            # print(cost)
            solutions.append(cost)

            count += 1
            # 判断是否接受该解
            if cost < min or random.random() < np.exp(-((cost - min) / t * k)):
                temp = path_nei
                min = cost
            if cost < result[1]:
                result = [path_nei, cost]
        # t/=math.log10(1+k)
        t /= 99 + 1  # 降温操作
    return result[0], result[1]


def main():
    global solutions, visited, size, map
    kmax = 1000
    t0 = 500000
    t_end = 0.00001
    start = tuple([k for k in range(size)])
    visited.update({start: getCost(start)})
    solutions.append(visited[start])
    time_start = time.time()
    global count
    count = 0
    path_, cost = SA(start, kmax, t0, t_end)
    path = path_[:] + path_[:1]
    time_end = time.time()
    print()
    print('Algorithm SA iterated', count, 'times!\n', sep=' ')
    print('It cost ', time_end - time_start, 's', sep='')  # 此处单位为秒
    print('Objective Value: ', cost)
    print(path)
    path1 = [str(city) for city in path]
    path_to_write = ' '.join(path1)
    print('Solution Vector：', path_to_write)
    best = 6528 # 手动设置
    print("误差为：", (cost - best) / best)
    x = np.array([map[i][0] for i in path])
    y = np.array([map[i][1] for i in path])
    i = np.arange(0, len(solutions))
    solutions = np.array(solutions)

    plt.figure(figsize=(16, 8))
    plt.subplot(121)
    plt.plot(x, y, '-o', markersize=5, linewidth=1)
    # 在第一个点上标注"start"
    plt.text(x[0], y[0], ' Start:' + str(path[0]), horizontalalignment='right', verticalalignment='bottom', fontsize=8,
             fontweight='bold', color='red')
    # 在其他点上标注它们的序号
    for idx in range(1, len(x) - 1):
        plt.text(x[idx], y[idx], f' {path[idx]}', horizontalalignment='right', verticalalignment='bottom', fontsize=8)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Path')

    plt.subplot(122)
    plt.xlabel('Iterations')
    plt.ylabel('Cost')
    plt.plot(i, solutions)
    plt.title('Iteration')
    plt.show()


main()
