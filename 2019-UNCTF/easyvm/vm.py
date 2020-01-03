#!/usr/bin/env python
unk_602080 = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF]
unk_6020A0 = [0xF4, 0x0A, 0xF7, 0x64, 0x99, 0x78, 0x9E, 0x7D, 0xEA, 0x7B, 0x9E, 0x7B, 0x9F, 0x7E, 0xEB, 0x71, 0xE8, 0x00, 0xE8, 0x07, 0x98, 0x19, 0xF4, 0x25, 0xF3, 0x21, 0xA4, 0x2F, 0xF4, 0x2F, 0xA6, 0x7C]

flag = []
for i in range(32):
    c = 0x1F - i
    b = unk_6020A0[c]
    a = b ^ 0xCD
    if c == 0:
        b = 0
    else:
        b = unk_6020A0[c - 1]
    a ^= b
    flag.append(a + c)
flag = flag[::-1]
print flag

a, b, c, d = 0, 0, 0, 0

sign = unk_602080[9]
while True:
    if sign == 0xA0:
        a += 1
    elif sign == 0xA1:
        b += 1
    elif sign == 0xA2:
        c += 1
        sign += 11
    elif sign == 0xA3:
        a -= c
        sign += 2
    elif sign == 0xA4:
        a ^= b
        sign += 7
    elif sign == 0xA5:
        b ^= a
        sign += 1
    elif sign == 0xA6:
        a = 0xCD
        sign -= 2
    elif sign == 0xA7:
        b = a
        sign += 7
    elif sign == 0xA8:
        c = 0xCD
    elif sign == 0xA9:
        a = flag[c]
        sign -= 6
    elif sign == 0xAA:
        b = flag[c]
    elif sign == 0xAB:
        if a > unk_6020A0[c]:
            d = 1
        elif a == unk_6020A0[c]:
            d = 0
        else:
            d = -1
        sign -= 4
    elif sign == 0xAC:
        if b > unk_6020A0[c]:
            d = 1
        elif b == unk_6020A0[c]:
            d = 0
        else:
            d = -1
    elif sign == 0xAD:
        if c > 0x1F:
            d = 1
        else:
            d = 0
        sign += 2
    elif sign == 0xAE:
        if d == 1:
            print 'wrong'
            break
        sign -= 12
    elif sign == 0xAF:
        if d == 1:
            print 'right'
            break
        sign -= 6
    else:
        print 'cmd execute error'
        break

flag = ''.join(chr(c) for c in flag)
print flag

