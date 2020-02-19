#!/usr/bin/env python
from des import *

part = '92d915250119e12b'.decode('hex')
keymap = 'e0be661032d5f0b676f82095e4d67623628fe6d376363183aed373a60167af537b46abc2af53d97485591f5bd94b944a3f49d94897ea1f699d1cdc291f2d9d4a5c705f2cad89e938dbacaca15e10d8aeaed90236f0be2e954a8cf0bea6112e84'.decode('hex')

keymap = convert_string_to_bitlist(keymap)
for i in range(16):
    sub_keys[i] = keymap[48*i:48*i+48]
print sub_keys

def bruteforce(block, n):
    rblock = block[:32]
    lblock = block[32:]
    i = n
    while i > 0:
        rtemp = rblock[:]
        rblock = permute(E, rblock)
        rblock = list(map(lambda x, y: x ^ y, rblock, sub_keys[i - 1]))
        b = [rblock[:6], rblock[6:12], rblock[12:18], rblock[18:24],
             rblock[24:30], rblock[30:36], rblock[36:42], rblock[42:]]
        j = 0
        bn = [0] * 32
        pos = 0
        while j < 8:
            row = (b[j][0] << 1) + b[j][5]
            col = (b[j][1] << 3) + (b[j][2] << 2) + (b[j][3] << 1) + b[j][4]
            v = S[j][(16 * row) + col]
            bn[pos] = (v & 8) >> 3
            bn[pos + 1] = (v & 4) >> 2
            bn[pos + 2] = (v & 2) >> 1
            bn[pos + 3] = v & 1
            pos += 4
            j += 1
        rblock = permute(P, bn)
        rblock = list(map(lambda x, y: x ^ y, rblock, lblock))
        lblock = rtemp
        i -= 1
    final = permute(IP_, rblock + lblock)
    return convert_bitlist_to_string(final)

part = convert_string_to_bitlist(part)
print part
for i in range(16):
    print bruteforce(part, i)

