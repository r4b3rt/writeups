#!/usr/bin/env python
import base64

def pos(x,y):
    for i in range(len(y)):
        if y[i] == x:
            return i

table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
enc = [0] * 36
enc[0] = ord(table[28])
enc[3] = ord('j')
enc[4] = enc[0] + 1
enc[12] = enc[4] - 1
enc[22] = enc[4] - 1
enc[24] = enc[4] - 1
enc[1] = ord(table[54])
enc[2] = ord(table[((28 + pos(chr(enc[1]), table)) >> 2) + 1])
enc[10] = enc[2]
enc[6] = enc[3] - 32
enc[7] = ord('p')
enc[11] = 48
enc[23] = 48
enc[35] = enc[11] + 9
enc[8] = enc[0] - 1 
enc[27] = enc[4] + 2
enc[31] = enc[27]
enc[9] = enc[27] + 7
enc[25] = enc[27] + 7
enc[13] = enc[1] + 1 
enc[17] = enc[1] + 1 
enc[21] = enc[1] + 1 
enc[15] = enc[7] + 3
enc[14] = enc[15] + 1 
enc[19] = ord('z')
enc[34] = enc[0] - 33
enc[5] = 88
enc[20] = 88
enc[29] = 88
enc[33] = 88
enc[26] = 49
enc[16] = enc[9] - 32
enc[28] = enc[16]
enc[18] = enc[7] - 30
enc[30] = enc[18]
enc[32] = enc[4]

flag = ''
for i in enc:
    flag += chr(i)
flag = base64.b64decode(flag)
print 'flag:', flag
