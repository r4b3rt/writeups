#!/usr/bin/env python
from pwn import *
import base64
context.log_level = 'debug'
# p = remote('110.10.147.104', 15712)
p = remote('110.10.147.109', 15712)
p.sendlineafter('If you want to start, type the G key within 10 seconds....>>', 'G')

def cal(m):
    size = len(m)
    res = []
    for i in range(size):
        res.append(m[i][size - 1])
    for i in range(size - 2, -1, -1):
        res[0] += m[0][i]
        for j in range(1, size):
            res[j] = min(res[j - 1] + m[j][i], res[j] + m[j][i])
        for j in range(size - 2, -1, -1):
            res[j] = min(res[j], res[j + 1] + m[j][i])
    return min(res)

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
    min_length = cal(matrix)
    flag += chr(min_length)
    payload = str(min_length)
    p.sendlineafter('Answer within 10 seconds >>>', payload)
print 'flag:', base64.b64decode(flag)
p.interactive()
