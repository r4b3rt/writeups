#!/usr/bin/env python
import base64

with open('flag.txt', 'rb') as f:
    ciphertext = f.read()

while True:
    try:
        ciphertext = base64.b64decode(ciphertext)
        print ciphertext
    except Exception:
        break

