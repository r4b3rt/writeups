#!/usr/bin/env python
fake = 'fL492_r_h4rd3r_th4n_th1s'
flag = ''
target = [58, 49, 82, 48, 52, 54, 82, 48, 51, 92, 58, 81, 115, 48, 53, 69, 92, 49, 90, 52]
for i in range(len(target)):
    flag += chr(((target[i] ^ 0x32) - 1) ^ 0x32)
print flag

