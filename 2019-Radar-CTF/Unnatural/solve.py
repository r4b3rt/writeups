#!/usr/bin/env python
with open('flag.txt', 'rb') as f:
    enc = f.read()
    for c in enc:
        print hex(ord(c))
