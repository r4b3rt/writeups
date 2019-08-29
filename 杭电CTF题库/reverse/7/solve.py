#!/usr/bin/env python
enc = 'asdfghjklq'
flag = ''
for i in range(9):
	flag += chr(ord(enc[i]) + 2)
print flag
