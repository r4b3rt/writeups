#!/usr/bin/env python

def decrypt(x):
    c = ((x << 7) | (x >> 57))&0xffffffffffffffff
    b = ((((c >> 32)&0xffffffff)-0xffc2bdec)&0xffffffff)^0xffc2bdec
    a = (((c&0xffffffff)-0xffc2bdec)&0xffffffff)^0xffc2bdec
    return ((a << 32) | b)&0xffffffffffffffff

flag = 0xd274a5ce60ef2dca
for i in xrange(0x7f):
    flag = decrypt(flag)

print hex(flag)
print hex(flag)[2:-1:].decode('hex')
