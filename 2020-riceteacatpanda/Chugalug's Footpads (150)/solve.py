#!/usr/bin/env python
with open('diff', 'rb') as f:
    diff = f.readlines()
flag = ''
for l in diff:
    print l[11:14]
    flag += chr(int(l[11:14], 8))
print flag

