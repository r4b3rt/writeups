#!/usr/bin/env python
import base64
enc = 'fYZ7ipGIjFtsXpNLbHdPbXdaam1PS1c5lQ=='
text = base64.b64decode(enc)
i = 0
while True:
    flag = ''
    for c in text:
        flag += chr((ord(c) + i) % 256)
    i += 1
    if 'encrypt' in flag:
        print flag
        exit()
