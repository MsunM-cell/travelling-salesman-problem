import matplotlib.pyplot as plt
import random
import numpy as np
import time
import elkai

# Read the city's x and y coordinates
def load_tsp(tsp):
    f = open(tsp)
    map = {}
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
            map[int(int(a[0]) - 1)] = (float(a[1]), float(a[2]))
    return map


# Gets the two-dimensional Euclidean distance between two cities
def get_distance():
    global city_map, city_size
    dist = np.zeros((city_size, city_size))
    for i in range(0, city_size):
        for j in range(0, city_size):
            dist[i][j] = ((city_map[i][0] - city_map[j][0]) ** 2 + (city_map[i][1] - city_map[j][1]) ** 2) ** 0.5
    return dist


tsp_file = "pr1002.tsp"
city_map = load_tsp(tsp_file)
city_size = len(city_map)
# visited = {}
# solutions = []
city_distance = get_distance()
# print(city_distance)
count = 0
# print(city_map)

cities = elkai.Coordinates2D(city_map)
print(cities)

res = cities.solve_tsp()
# print(res)

cost = 0
former = res[0]
for city in res:
    cost += city_distance[former][city]
    former = city
# print(cost)

print('Objective Value：', cost)
path1 = [str(city + 1) for city in res]
path_to_write = ' '.join(path1)
print('Solution Vector：', path_to_write)

x = np.array([city_map[i][0] for i in res])
y = np.array([city_map[i][1] for i in res])
plt.plot(x, y, '-o', markersize=5, linewidth=1)
# 在第一个点上标注"start"
plt.text(x[0], y[0], ' Start:' + str(res[0]), horizontalalignment='right', verticalalignment='bottom', fontsize=8,
         fontweight='bold', color='red')
# 在其他点上标注它们的序号
for idx in range(1, len(x) - 1):
    plt.text(x[idx], y[idx], f' {res[idx]}', horizontalalignment='right', verticalalignment='bottom', fontsize=8)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Path')
plt.show()



