#!/usr/bin/env python
with open('RSA.py', 'r') as f:
    content = f.read()

res = ''
for c in content:
    if c == chr(0x0D):
        res += '\n'
    else:
        res += c
print res

