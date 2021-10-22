#!/usr/bin/env python
import string

table = string.printable

with open('opt.txt', 'r') as f:
    vals = f.readlines()

with open('opt.txt.ori', 'r') as f:
    cipher = f.readlines()

flag = ''
for c in cipher:
    for i in range(len(vals)):
        if c == vals[i]:
            flag += table[i]
print flag

