#!/usr/bin/env python
enc = '437261636b4d654a757374466f7246756e'
flag = ''
for i in range(len(enc) / 2):
    flag += chr(int(enc[2 * i:2 * i + 2], 16))
print flag
