#!/usr/bin/env python
import re

pat = re.compile(r'/\*.{1,10}\*/')
with open('README.md', 'rb') as f:
    content = f.read()
    res = pat.findall(content)
    print res
flag = ''
for l in res:
    flag += l[2:-2]
print flag

