#!/usr/bin/env python
with open('CipherText', 'rb') as f:
    enc = f.read()
    bits = ''
    for c in enc:
        if c == '-':
            bits += '1'
        elif c == '_':
            bits += '0'
    m = hex(int(bits, 2))[2:-1]
    print m
    flag = m.decode('hex').decode('hex')
    print flag
