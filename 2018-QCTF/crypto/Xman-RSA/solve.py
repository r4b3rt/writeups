#!/usr/bin/env python
import base64
import gmpy2
f = open('n2&n3', 'rb')
n2 = f.readline()
n3 = f.readline()
f.close()
n2 = base64.b64decode(n2).encode('hex')
n3 = base64.b64decode(n3).encode('hex')
n2 = int(n2, 16)
n3 = int(n3, 16)
# print 'n2:', n2
# print 'n3:', n3
# first step: solve n1
e1 = 0x1001
e2 = 0x101
f = open('n1.encrypted', 'rb')
n1_c1 = f.readline()
n1_c2 = f.readline()
f.close()
n1_c1 = int(n1_c1, 16)
n1_c2 = int(n1_c2, 16)
# print 'n1_c1:', n1_c1
# print 'n1_c2:', n1_c2
gcd, s, t = gmpy2.gcdext(e1, e2)
if s < 0:
    s = abs(s)
    n1_c1 = gmpy2.invert(n1_c1, n3)
if t < 0:
    t = abs(t)
    n1_c2 = gmpy2.invert(n1_c2, n3)
n1 = gmpy2.powmod(n1_c1, s, n3) * gmpy2.powmod(n1_c2, t, n3) % n3
print 'n1:', n1
# second step: solve flag
f = open('ciphertext', 'rb')
c1 = f.readline()
c2 = f.readline()
f.close()
c1 = int(c1, 16)
c2 = int(c2, 16)
print 'c1:', c1
print 'c2:', c2
e = 0x1001
p1 = gmpy2.gcd(n1, n2)
p2 = n1 / p1
p3 = n2 / p1
d1 = gmpy2.invert(e, (p1 - 1) * (p2 - 1))
d2 = gmpy2.invert(e, (p1 - 1) * (p3 - 1))
m1 = pow(c1, d1, n1)
m2 = pow(c2, d2, n2)
msg1 = hex(m1)[2:].decode('hex')
msg2 = hex(m2)[2:].decode('hex')
flag = ''
for i in range(len(msg1 + msg2)):
    if i % 2 == 0:
        flag += msg1[i / 2]
    else:
        flag += msg2[i / 2]
print 'flag:', flag
