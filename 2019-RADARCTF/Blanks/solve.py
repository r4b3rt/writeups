#!/usr/bin/env python
with open('flag.txt', 'rb') as f:
    enc = f.read().encode('hex')
    bits = enc.replace('09', '0').replace('20', '1')
    print bits
    flag = ''
    for i in range(len(bits) / 8):
        flag += chr(int(bits[8 * i:8 * i + 8], 2))
    print flag
