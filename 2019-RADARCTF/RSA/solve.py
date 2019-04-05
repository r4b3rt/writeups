#!/usr/bin/env python
import base64
import gmpy2
n = 7576962585305391589
p = 2045145391
q = 3704852779
phi = (p - 1) * (q - 1)
e = 65537
d = gmpy2.invert(e, phi) # 4406608918927534373
f = open('RSA.txt', 'r')
content = f.readlines()[4:]
msg = ''
for i in content:
    ch = ''
    m = gmpy2.powmod(int(i), d, n)
    a = m / 10000
    b = (m - a * 10000) / 100
    c = (m - a * 10000 - b * 100)
    ch = chr(a) + chr(b) + chr(c)
    msg += ch
print msg
m = base64.b32decode(msg)
print m
m = m.split(' ')
flag = ''
for c in m:
    flag += chr(int(c))
print flag

