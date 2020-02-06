#!/usr/bin/env python
import libnum

data = [0x57635565, 0x06530401, 0x1F494949, 0x5157071F, 0x575F4357, 0x57435E57, 0x4357020A, 0x575E035E, 0x0F590000, 0x00000000]

def solve():
    flag = ''
    for i in range(9):
        flag += libnum.n2s(data[i] ^ ((data[i] << 8) & 0xFFFFFFFF))[::-1]
        data[i + 1] = data[i] ^ data[i + 1]
    print flag

if __name__ == '__main__':
    solve()

