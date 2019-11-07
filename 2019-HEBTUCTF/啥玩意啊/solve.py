#!/usr/bin/env python
import hashlib
import string

def getflag1():
    flag1 = 'odm'
    for a in range(97, 123):
        for b in range(48, 58):
            tail = chr(a) + chr(b)
            h = hashlib.sha1(flag1 + tail).hexdigest()
            if h == '8af093ec12abbd25a82abd6d5ed8080afbbfa098':
                flag1 = flag1 + tail
                return flag1

flag1 = getflag1()
print flag1

flag2 = 'hello' # helxlo
print flag2

key1 = 5
key1_ = 21
key2 = 3
c = 'srpnv'
ciphertext = []
for i in range(len(c)):
    ciphertext.append(string.lowercase.find(c[i]))
print ciphertext

plaintext = []
for i in range(len(ciphertext)):
    plaintext.append((key1_ * (ciphertext[i] - key2)) % 26)
print plaintext
flag3 = ''
for i in range(len(plaintext)):
    flag3 += string.lowercase[plaintext[i]]
print flag3

flag = 'hebctf{' + flag1 + '-' + flag2 + '-' + flag3 + '}'
print flag

