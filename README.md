# travelling-salesman-problem
This project provides 4 algorithms to solve the famous travelling-salesman-problem(TSP),
including VNS, SA, GA, and LKH.
For example, you can modify the code in line 35 to input your tsp file.
```
tsp_file = "att48.tsp" # your tsp file
```
After get the target path and cost, you can compare it with the best result which can be available in [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/).

Note: I use the Python library [elkai](https://github.com/fikisipi/elkai) based on LKH 3 to solve the TSP. In my practice, it is very fast and accurate so I recommend the elkai very much.
```
pip install elkai
```
