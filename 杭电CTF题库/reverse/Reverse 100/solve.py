#!/usr/bin/env python
enc = '065ca>01??ab7e0f4>>a701c>cd17340'
flag = ''
for i in range(len(enc)):
	flag += chr(ord(enc[i]) ^ 7)
print flag
