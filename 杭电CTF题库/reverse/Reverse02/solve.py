#!/usr/bin/env python
enc = '7e0cad17016b0>?45?f7c>0>4a>1c3a0'
flag = ''
for i in range(len(enc)):
	flag += chr(ord(enc[i]) ^ 7)
print flag
