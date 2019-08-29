#!/usr/bin/env python
k = [2, 5, 9, 6, 7, 0, 0xA, 8, 0xC, 0xB, 3, 4, 1]
t = 'oFen'[::-1] + 'Ieil'[::-1] + 'HTrh'[::-1] + 'e'
flag = ''
for i in range(13):
	flag += t[k[i]]
print flag
