#!/usr/bin/env python
data = [0x00000066, 0x0000006D, 0x00000063, 0x00000064, 0x0000007F, 0x00000037, 0x00000035, 0x00000030, 0x00000030, 0x0000006B, 0x0000003A, 0x0000003C, 0x0000003B, 0x00000020]
res = []
for i in range(56 >> 2):
    res.append(i ^ data[i])
data2 = [0x00000037, 0x0000006F, 0x00000038, 0x00000062, 0x00000036, 0x0000007C, 0x00000037, 0x00000033, 0x00000034, 0x00000076, 0x00000033, 0x00000062, 0x00000064, 0x0000007A]
res2 = []
for i in range(1, 0x38 >> 2):
    res2.append(data[i] ^ data2[i] ^ data[i - 1])
res2 = [data2[0]] + res2
data3 = [0x0000001A, 0x00000000, 0x00000000, 0x00000051, 0x00000005, 0x00000011, 0x00000054, 0x00000056, 0x00000055, 0x00000059, 0x0000001D, 0x00000009, 0x0000005D, 0x00000012]
res3 = []
for i in range((56 >> 2) - 1):
    res3.append(i ^ (data3[i + 1] ^ res2[i]))
res3 = [data3[0] ^ data2[0]] + res3
flag = ''
for i in range(len(res)):
    flag += chr(res[i])
for i in range(len(res2)):
    flag += chr(res2[i])
for i in range(len(res3)):
    flag += chr(res3[i])
print flag

