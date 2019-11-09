#!/usr/bin/env python
import base64
with open('flag.txt', 'rb') as f:
    content = f.readlines()
    output = ''
    for i in range(len(content)):
        output += content[i][i]
    print output
    if len(output) % 3 == 1:
        output += '=='
    elif len(output) % 3 == 2:
        output += '='
    flag = base64.b64decode(output)
    print flag
