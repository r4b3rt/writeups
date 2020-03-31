#!/usr/bin/env python
from pwn import *

table = [chr(c) for c in range(0x20, 0x7F)]

for c in table:
	print c, disasm(c + 'ABCDEFG').split('\n')[0][6:]

