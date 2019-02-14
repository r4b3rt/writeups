#!/usr/bin/env python

def encrypt(x):
    a = x >> 32
    a ^= 0xffc2bdec
    a += 0xffc2bdec
    a &= 0xffffffff

    b = x & 0xffffffff
    b ^= 0xffc2bdec
    b += 0xffc2bdec
    b &= 0xffffffff

    c = ((b << 32) | a)&0xffffffffffffffff
    d = ((c & 0x7f) << 57)&0xffffffffffffffff

    return ((c >> 7) | d) & 0xffffffffffffffff

flag = str(input())
flag = int('0x' + flag.encode('hex'), 16)

for i in range(0x7f):
    flag = encrypt(flag)

print hex(flag)
