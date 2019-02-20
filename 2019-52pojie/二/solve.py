#!/usr/bin/env python
enc = ('9102' + 'udhY' + 'zhNb' + 'ssdH')[::-1]
print enc
alpha = 'abcdefghijklmnopqrstuvwxyz'
num = 3
t = alpha[num + 1]
i = len(enc)
j = 0
res = ''
while i != 0:
    c = enc[j]
    if ord(c) < ord(t) or ord(c) > 122:
        if ord(c) >= 97 and ord(c) <= ord(alpha[num]):
            c = chr(ord(c) - num + 26)
            if ord(c) > ord(alpha[-1]):
                c = chr(ord(c) - 26)
    else:
        c = chr(ord(c) - num)
    res += c
    j += 1
    i -= 1
print res
# HappyNewYear2019