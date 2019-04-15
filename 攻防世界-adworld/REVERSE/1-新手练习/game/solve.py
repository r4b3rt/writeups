#!/usr/bin/env python
import re
with open('chars', 'rb') as f:
    content = f.readlines()
    regex = re.compile(r'= (\d+);')
    output = []
    for i in range(len(content)):
        output.append(regex.findall(content[i])[0])
    # print output
    print len(output)
    v2 = output[57:]
    v59 = output[:57]
    # print v2
    # print v59
    flag = ''
    for i in range(len(v2)):
        flag += chr(int(v2[i]) ^ int(v59[i]) ^ 0x13)
    print flag
