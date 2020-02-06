#!/usr/bin/env python
#http://soreatu.com/ctf/writeups/Writeup%20for%20warmup%20in%202019%E5%9B%BD%E8%B5%9B.html
from pwn import *
import libnum

context.log_level = 'debug'

#r = remote('fc32f84bc46ac22d97e5f876e3100922.kr-lab.com', 12345)
r = remote('127.0.0.1', 7777)

def retrieve(payload=''):
    r.sendline(payload)
    r.recvuntil('result>')
    data = r.recvline()[:-1]
    info(data)
    return data.decode('hex')

m1 = ''
c1 = retrieve()
m2 = 'x' * 50
c2 = retrieve(m2)
r.close()

flag = ''
for i in range(len(c1)):
    flag += chr(ord(c1[i]) ^ ord(c2[i]) ^ ord('x'))
print flag

