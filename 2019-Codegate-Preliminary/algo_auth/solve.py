#!/usr/bin/env python
from pwn import *
import numpy as np
import base64
context.log_level = 'debug'
# p = remote('110.10.147.104', 15712)
p = remote('110.10.147.109', 15712)
p.sendlineafter('If you want to start, type the G key within 10 seconds....>>', 'G')

def minDistance(distances, sptSet, dimension):
    min_ = np.inf
    min_index = 0
    for i in range(dimension):
        if sptSet[i] == False and distances[i] < min_:
            min_ = distances[i]
            min_index = i
    return min_index

def dijkstra(graph, source, dimension): 
    sptSet = []
    distances = []
    for i in range(dimension):
        distances.append(np.inf)
        sptSet.append(False)
    distances[source] = 0
    for i in range(dimension):
        u = minDistance(distances, sptSet, dimension)
        sptSet[u] = True
        for v in range(dimension):
            if sptSet[v] == False and graph[u][v] > 0 and distances[u] + graph[u][v] < distances[v]:
                distances[v] = distances[u] + graph[u][v]
    # print distances
    res = []
    for i in range(1, 8):
        res.append(distances[i * 7 - 1])
    print res
    return res

def xy2num(x, y):
    if x < 0 or x >= 7:
        return -1
    if y < 0 or y >= 7:
        return -1
    return y * 7 + x

flag = ''

for i in range(100):
    p.recvuntil('*** STAGE {} ***\n'.format(str(i + 1)))
    matrix = []
    for j in range(7):
        t = p.recvline()[:-1]
        row = []
        for k in range(len(t) / 3):
            # print type(t[3*k:3*(k+1)].strip(' '))
            row.append(int(t[3*k:3*(k+1)].strip(' ')))
        matrix.append(row)
    # print matrix
    min_length = np.inf
    adj = []
    for y in range(7):
        for x in range(7):
            t = [0] * (7 * 7)
            if xy2num(x - 1, y) >= 0:
                t[xy2num(x - 1, y)] = matrix[y][x - 1]
            if xy2num(x + 1, y) >= 0:
                t[xy2num(x + 1, y)] = matrix[y][x + 1]
            if xy2num(x, y - 1) >= 0:
                t[xy2num(x, y - 1)] = matrix[y - 1][x]
            if xy2num(x, y + 1) >= 0:
                t[xy2num(x, y + 1)] = matrix[y + 1][x]
            adj.append(t)
    for j in range(7):
        tmp = min(dijkstra(adj, j * 7, 7 * 7))
        tmp += matrix[j][0]
        min_length = min(min_length, tmp)
    flag += chr(min_length)
    payload = str(min_length)
    p.sendlineafter('Answer within 10 seconds >>>', payload)
print 'flag:', base64.b64decode(flag)
p.interactive()
