# Simple Single Loop Topology:
# 1 --- 2  +--5
# |     | /   |
# |     |/    |
# 3 --- 4 --- 6

topo = {1: [2, 3],
        2: [1, 4],
        3: [1, 4],
        4: [2, 3, 5, 6],
        5: [4, 6],
        6: [4, 5]}
