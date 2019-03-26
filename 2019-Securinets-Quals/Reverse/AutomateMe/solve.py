#!/usr/bin/env python
import re
with open('bin.c', 'rb') as f:
    txt = f.read()
    regex = re.compile(r'\'(.*)\'')
    # print regex.findall(txt)
    output = ''
    for c in regex.findall(txt):
        output += c
    print output
