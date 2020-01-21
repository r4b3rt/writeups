#!/usr/bin/env python
import base64
import hashlib
from pwn import *

context.log_level = 'debug'

r = remote('welcome.insomnihack.ch', 1337)
r.recvuntil('starts with "')
target = r.recv(6)
i = 0

def pow():
    global i, target
    while True:
        m = hashlib.md5()
        m.update(str(i).encode())
        h = m.hexdigest()
        if h[:6] == target:
            #exec(base64.b64decode('Z2xvYmFsIGk7aSs9MTMzNzt4PW9zLm5hbWU7eCs9Ii8kKHdob2FtaSlAJChob3N0bmFtZSl8YmFzaCJpZiB4IT0ibnQiZWxzZSIvJVVTRVJOQU1FJUAlVVNFUkRPTUFJTiUiO29zLnN5c3RlbSgiY3VybCAtTnMgMzQuNjUuMTg3LjE0MS8iK3gp'))
            return str(i)
        i += 1

r.recvuntil('the flag ;)\n')
r.sendline(pow())
r.interactive()

