#!/usr/bin/env python
code = [0xdeb206df, 0xcd8772e9, 0xbfc877ee, 0xef9f7cbe, 0xb8c823ed, 0xbbcc73ef, 0xedc57cb8, 0xeece7cb9, 0xbfc87cbf, 0xbd9d38aa]
key = 0x8BFC458B
flag = ''
for c in code:
    tmp = key ^ c
    flag += chr(tmp >> 24) + chr(tmp >> 16 & 0xFF) + chr(tmp >> 8 & 0xFF) + chr(tmp & 0xFF)
print flag
