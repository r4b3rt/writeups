#!/usr/bin/env python
from pwn import *
context.terminal = ['tmux', 'sp', '-h']
context.log_level = 'debug'
local = 0
if local:
	p = process('./crackme03')
else:
	p = remote('104.154.106.182', 7777)
# gdb.attach(p)
# input #0
p.recvuntil('input #0:')
p.sendline('CRACKME02')
# input #1
p.recvuntil('input #1:')
p.sendline(p32(0xdeadbeef))
# input #2
p.recvuntil('input #2:')
p.sendline('ZXytUb9fl78evgJy3KJN')
# input #3
p.recvuntil('input #3:')
for num in range(1000):
	if num ** 3 + 2 * (2 * (num ** 2) - num) - 3 == 0:
		break
p.sendline(str(num))
# input #4
p.recvuntil('input #4:')
payload = ''
payload += chr(97)
payload += chr(98)
payload += chr(120)
payload += chr(100)
payload += chr(105)
payload += chr(201 - 100)
payload += chr(231 - 120)
payload += chr(206 - 98)
payload += chr(213 - 97)
p.sendline(payload[::-1])
p.interactive()
