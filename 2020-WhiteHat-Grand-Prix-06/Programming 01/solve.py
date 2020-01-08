#!/usr/bin/env python
#https://blog.csdn.net/wu_tongtong/article/details/78319149
from pwn import *

context.log_level = 'debug'
r = remote('15.164.75.32', 1999)

answer = {}
answer[3] = 0
for i in range(4, 1000001):
    answer[i] = answer[i - 1] + ((i - 1) * (i - 2) / 2 - (i - 1) / 2) / 2

while True:
    r.recvuntil('n = ')
    n = int(r.recvuntil('\n')[:-1])
    info('n = ' + str(n))
    res = answer[n]
    r.recvuntil('Answer: ')
    r.sendline(str(res))

r.interactive()

