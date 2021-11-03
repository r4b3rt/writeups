#!/usr/bin/env python
check1 = '1f03d3ddd728d543fd11c7211190d5b7'

check2 = ''
for i in range(4):
    for j in range(8):
        check2 += check1[8 * i + j]

check3 = ''
for i in range(8):
    check3 += check2[8 + i]
    check3 += check2[24 + i]
    check3 += check2[16 + i]
    check3 += check2[i]

check4 = ''
for i in range(8):
    check4 += check3[4 * i + 2]
    check4 += check3[4 * i + 3]
    check4 += check3[4 * i]
    check4 += check3[4 * i + 1]

flag = check4[::-1]
flag = 'HEBTUCTF{' + flag + '}'
print flag

