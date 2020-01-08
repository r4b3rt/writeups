#!/usr/bin/env sage -python
from utils import *
from sage.all import *

pos = {
    '1':['6', '8'],
    '2':['7', '9'],
    '3':['4', '8'],
    '4':['3', '9', '0'],
    '5':['*', '#'],
    '6':['1', '7', '0'],
    '7':['2', '6', '#'],
    '8':['1', '3'],
    '9':['2', '4', '*'],
    '*':['5', '9'],
    '0':['4', '6'],
    '#':['5', '7'],
}

r = remote('15.165.30.141', 9399)

R = Integers(10**39)
start = vector(R, [2, 0, 0, 1])
mat = Matrix(R, [
    [0, 0, 1, 2],
    [0, 0, 1, 0],
    [1, 2, 1, 0],
    [1, 0, 0, 0],
])

def get_answer(n):
    return int(sum((mat ** (n - 1)) * start))

flag = ''

while True:
    r.recvuntil('n = ')
    n = int(r.recvuntil('\n')[:-1])
    res = get_answer(n)
    r.recvuntil('Answer: ')
    r.sendline(str(res))
    r.recvuntil('your reward: ')
    flag += r.recv(1)
    print '[*]', flag
    if flag[-1] == '}':
        break

