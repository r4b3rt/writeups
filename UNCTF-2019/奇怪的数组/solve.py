#!/usr/bin/env python
enc = [0x000000AD, 0x00000046, 0x0000001E, 0x00000020, 0x0000003C, 0x00000079, 0x00000075, 0x000000B3, 0x0000005E, 0x00000052, 0x00000079, 0x00000060, 0x000000CB, 0x000000FE, 0x000000B0, 0x0000006C]
flag = ''
for i in range(len(enc)):
    flag += hex(enc[i] >> 4 & 0xF)[2:]
    flag += hex(enc[i] & 0xF)[2:]
flag = 'flag{' + flag + '}'
print flag

