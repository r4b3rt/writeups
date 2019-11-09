#!/usr/bin/env python
with open('flag.zip', 'rb') as f:
    content = f.read()
    output = ''
    for i in range(len(content) / 2):
        output += content[2 * i + 1]
        output += content[2 * i]
with open('output.zip', 'wb') as f:
    f.write(output)
