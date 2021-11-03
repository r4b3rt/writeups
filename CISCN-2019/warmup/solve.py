#!/usr/bin/env python
#https://www.ctfwp.com/articals/2019national.html#warmup
from pwn import *
import string

#r = remote('fc32f84bc46ac22d97e5f876e3100922.kr-lab.com', 12345)
r = remote('127.0.0.1', 7777)

def exp(idx, flag):
    for i in range(idx, len(table)):
        payload = flag + table[i]
        r.sendline(payload)
        data = r.recvline()[17:][:-1][:(len(flag) + 1) * 2]
        if data in result:
            print payload
            exp(0, payload)

flag = 'flag'
table = string.printable
r.recvuntil('Welcome to flag getting system\n')
r.sendline()
result = r.recvline()[17:][:-1]
exp(0, flag)

r.interactive()

