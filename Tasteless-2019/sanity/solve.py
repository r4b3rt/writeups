#!/usr/bin/env python
from hashlib import sha1
from pwn import *

context.log_level = 'debug'

def proof(t, prefix):
    i = 0
    while True:
        if sha1(str(t + str(i)).encode()).hexdigest().startswith(prefix):
            return str(i)
        i += 1

r = remote('hitme.tasteless.eu', 10001)
while True:
    r.recvuntil('sha1(')
    data = r.recvuntil(',')[:-1]
    info(data)
    r.recvuntil('prefix = ')
    prefix = r.recvuntil('...')[:-3]
    info(prefix)
    res = proof(data, prefix)
    info(res)
    r.sendline(res)

