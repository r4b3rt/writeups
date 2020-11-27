#!/usr/bin/env python
import hashlib

key = 'thisiskey52pojie_2020_happy_chinese_new_year20200125'
key1 = key[:0x7D-0x74]
key2 = key[0x7D-0x74:0xA0-0x74]
key3 = key[0xA0-0x74:]

arr = ''
for i in range(35):
    if not i or i & 3:
        arr += key2[i]
    else:
        arr += key3[(i >> 2) - 1]
print arr

md5str = hashlib.md5(arr).digest()
print md5str.encode('hex')

xorlist = []
for i in range(16):
    xorlist.append(ord(key1[i % 9]) ^ ord(md5str[i]))
print xorlist

flag = ''
for i in range(16):
    flag += hex(xorlist[i])[2:].zfill(2)
print flag
flag = flag[1:31]
print flag
assert len(flag) == 30

