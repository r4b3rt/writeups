#!/usr/bin/env python
from pwn import *

flag = [[i for i in range(0x100)] for j in range(37)]

while not all([len(a) == 1 for a in flag]):
    print flag
    try:
        #r = remote('hitme.tasteless.eu', 10401)
        r = remote('127.0.0.1', 8888)
        ciphertext = r.recvall()
        r.close()
        for i in range(37):
            if ord(ciphertext[i]) in flag[i]:
                flag[i].remove(ord(ciphertext[i]))
    except EOFError:
        continue
    except Exception:
        continue

flag = ''.join(chr(c[0]) for c in flag)
print flag

