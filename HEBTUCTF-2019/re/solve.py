#!/usr/bin/env python
import hashlib

with open('enc.bin', 'rb') as f:
    enc = f.read()
enc = [ord(enc[i]) for i in range(len(enc))]
enc = [74, 97, 112, 128, 158, 180, 206, 253, 189, 132, 248, 233, 4, 105, 115, 41, 196, 61, 224, 106, 43, 238, 99, 5, 235, 137, 87, 126, 4, 100, 211, 248]



