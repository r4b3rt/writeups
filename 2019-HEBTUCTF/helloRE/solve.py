#!/usr/bin/env python
import base64

data = [0x61, 0x59, 0x39, 0x29, 0x5A, 0x28, 0x3F, 0x7C, 0x5A, 0x58, 0x39, 0x78, 0x4F, 0x43, 0x39, 0x7A, 0x5F, 0x69, 0x39, 0x65, 0x4F, 0x59, 0x43, 0x77, 0x00]
for i in range(len(data)):
    if data[i] < 0x26 and data[i] > 0x1D:
        data[i] += 1
    if data[i] >= 0x73 and data[i] <= 0x7D:
        data[i] -= 3
    if data[i] >= 0x5D and data[i] <= 0x6B:
        data[i] += 4
    if data[i] >= 0x4F and data[i] < 0x5C:
        data[i] -= 2
    if data[i] >= 0x3E and data[i] <= 0x49:
        data[i] += 3
    if data[i] >= 0x28 and data[i] < 0x30:
        data[i] += 8

flag = ''
for i in range(len(data)):
    flag += chr(data[i])
flag = list(flag)
flag[8] = 'Z'
flag = ''.join(flag)
flag = 'flag{' + base64.b64decode(flag) + '}'
print flag

