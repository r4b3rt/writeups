#!/usr/bin/env python
#https://ctftime.org/writeup/17984
import base64
param = base64.b64decode('rJ/1g5PA5amy176A64akjuq/jryOug==')
key = 'e5d1a6f8c1f0d5ddf9e6cac6dbf4f6e1dad4e7d9fdc7a5fcc8c4e4dee3a2f7c5fea3ffd0c3e0abc2a7d8d7e2dfebdcaaa1a0d3cba4f1fac0fbf5d6f3eae8'.decode('hex')
flag = ''
for i in range(len(param)):
    flag += chr(ord(param[i]) ^ ord(key[i % len(key)]))
print flag
# INS{R00tK1tF0rRo0kies}
