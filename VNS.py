import matplotlib.pyplot as plt
import random
import numpy as np
import time


# Read the city's x and y coordinates
def load_tsp(tsp):
    f = open(tsp)
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


# Gets the two-dimensional Euclidean distance between two cities
def get_distance():
    global city_map, city_size
    dist = np.zeros((city_size, city_size))
    for i in range(0, city_size):
        for j in range(0, city_size):
            dist[i][j] = ((city_map[i][0] - city_map[j][0]) ** 2 + (city_map[i][1] - city_map[j][1]) ** 2) ** 0.5
    return dist


tsp_file = "att48.tsp"
city_map = load_tsp(tsp_file)
city_size = len(city_map)
visited = {}
solutions = []
city_distance = get_distance()
count = 0
print(city_distance)

# Gets the total cost of the path based on the path
def get_cost(path):
    cost = 0
    former = path[0]
    for city in path:
        cost += city_distance[former][city]
        former = city
    cost += city_distance[path[0]][path[-1]]
    return cost


# The perturbation generates a new random solution, which is randomly sorted into four intervals
def shaking(path):
    global city_size
    init_cost = visited[path]
    cnt = 0
    while True:
        pos1, pos2, pos3 = sorted(random.sample(range(0, city_size), 3))
        path_new = path[pos1:pos2] + path[:pos1] + path[pos3:] + path[pos2:pos3]
        if path_new not in visited:
            cost = get_cost(path_new)
            visited.update({path_new: cost})
        else:
            cost = visited[path_new]
        cnt += 1
        if init_cost >= cost:
            break
        elif cnt > 100:
            path_new = path
            cost = init_cost
            break
    return path_new


# 2-opt
def get_neighbor_2opt(path):
    global city_size
    min = visited[path]
    cnt = 0
    while True:
        i, j = sorted(random.sample(range(1, city_size - 1), 2))
        path_new = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
        if path_new not in visited:
            cost = get_cost(path_new)
            visited.update({path_new: cost})
        else:
            cost = visited[path_new]
        cnt += 1
        if cost < min:
            min = cost
            break
        elif cnt > 1000:
            path_new = path
            break
    return path_new, min


# exchange
def get_neighbor_exchange(path):
    global city_size
    min = visited[path]
    cnt = 0
    while True:
        i, j = sorted(random.sample(range(1, city_size - 1), 2))
        path_new = path[:i] + path[j:j + 1] + path[i + 1:j] + path[i:i + 1] + path[j + 1:]
        if path_new not in visited:
            cost = get_cost(path_new)
            visited.update({path_new: cost})
        else:
            cost = visited[path_new]
        cnt += 1
        if cost < min:
            min = cost
            break
        elif cnt > 1000:
            path_new = path
            break
    return path_new, min


# insert
def get_neighbor_insert(path):
    global city_size
    min = visited[path]
    cnt = 0
    while True:
        i, j = sorted(random.sample(range(1, city_size - 1), 2))
        path_new = path[i:i + 1] + path[j:j + 1] + path[:i] + path[i + 1:j] + path[j + 1:]
        if path_new not in visited:
            cost = get_cost(path_new)
            visited.update({path_new: cost})
        else:
            cost = visited[path_new]
        cnt += 1
        if cost < min:
            min = cost
            break
        elif cnt > 1000:
            path_new = path
            break
    return path_new, min


# VND: Variable Neighborhood Descent
def VND(path):
    l = 0
    min = visited[path]
    while l < 3:
        if l == 0:
            path_new, cost = get_neighbor_2opt(path)
        elif l == 1:
            path_new, cost = get_neighbor_exchange(path)
        elif l == 2:
            path_new, cost = get_neighbor_insert(path)
        if cost < min:
            path = path_new
            min = cost
            l = 0
        else:
            l += 1
    return path, min


# VNS: Variable Neighborhood Search
def VNS(path, kmax):
    k = 0
    temp = path
    min = solutions[0]
    global count
    while k < kmax:
        # VN is performed after perturbation
        path_neighbor, cost = VND(shaking(temp))
        # print(cost)
        solutions.append(cost)
        count += 1
        if cost < min:
            temp = path_neighbor
            min = cost
            k = 0
        else:
            k += 1
    return temp, min


def main():
    time_start = time.time()
    global solutions, visited, city_size, city_map
    kmax = 1000
    start = tuple([k for k in range(city_size)])
    visited.update({start: get_cost(start)})
    solutions.append(visited[start])
    path_final, cost = VNS(start, kmax)
    path = path_final[:] + path_final[:1]
    time_end = time.time()
    print()
    print('Algorithm VNS iterated', count, 'times!\n', sep=' ')
    print('It cost ', time_end - time_start, 's', sep='')
    print('You got the best solution:', cost, sep='\n')
    print(path)

    best = int(input("The best solution should be: "))
    print("error: ", (cost - best) / best)
    x = np.array([city_map[i][0] for i in path])
    y = np.array([city_map[i][1] for i in path])
    i = np.arange(0, len(solutions))
    solutions = np.array(solutions)
    plt.subplot(121)
    plt.plot(x, y)
    plt.subplot(122)
    plt.plot(i, solutions)
    plt.show()

main()
