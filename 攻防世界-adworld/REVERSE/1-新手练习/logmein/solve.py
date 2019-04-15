#!/usr/bin/env python
enc = ':\"AL_RT^L*.?+6/46'
v7 = '65626D61726168'
table = []
for i in range(len(v7) / 2):
    table.append(int(v7[2 * i:2 * i + 2], 16))
table = table[::-1]
print table
flag = ''
for i in range(len(enc)):
    flag += chr(table[i % 7] ^ ord(enc[i]))
print flag
