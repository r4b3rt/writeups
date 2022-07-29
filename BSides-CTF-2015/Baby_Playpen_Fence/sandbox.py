#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF("./babypf")

context.binary = elf

s = lambda senddata : p.send(senddata)
sa = lambda recvdata, senddata : p.sendafter(recvdata, senddata)
sl = lambda senddata : p.sendline(senddata)
sla = lambda recvdata, senddata : p.sendlineafter(recvdata, senddata)
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata, timeout=timeout)
uu32 = lambda data : u32(data, signed='unsigned')
uu64 = lambda data : u64(data, signed='unsigned')
iu32 = lambda data : u32(data, signed='signed')
iu64 = lambda data : u64(data, signed='signed')
up32 = lambda data : p32(data, signed='unsigned')
up64 = lambda data : p64(data, signed='unsigned')
ip32 = lambda data : p32(data, signed='signed')
ip64 = lambda data : p64(data, signed='signed')

p = process(['seccomp-tools', 'dump', elf.path])

sh = asm('''
    xor rax, rax
''')
sa('LOAD PROGRAM\n', up32(len(sh)))
p.sendline(sh)

p.interactive()

