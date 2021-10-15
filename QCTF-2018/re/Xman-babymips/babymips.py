#!/usr/bin/env python
enc1 = 'Q|j{g'
enc2 = '\x52\xfd\x16\xa4\x89\xbd\x92\x80\x13\x41\x54\xa0\x8d\x45\x18\x81\xde\xfc\x95\xf0\x16\x79\x1a\x15\x5b\x75\x1f'
flag = ''
for i in range(5):
    ch = ord(enc1[i]) ^ (32 - i)
    print 'index', i, '==>', chr(ch)
    flag += chr(ch)
for i in range(5, 32):
    for ch in range(256):
        t = ch ^ (32 - i)
        if i % 2 == 0:
            res = ((t << 2) & 0xff) | (t >> 6)
        else:
            res = (t >> 2) | ((t << 6) & 0xff)
        if res == ord(enc2[i - 5]):
            print 'index', i, '==>', chr(ch)
            flag += chr(ch)
            break
print len(flag)
print 'flag:', flag
