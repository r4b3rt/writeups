#!/usr/bin/env python3
from pwn import *

#context.log_level = 'debug'

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

p = remote('pwnable.kr', 9007)

ru('\t- Ready? starting in 3 sec... -\n')
sleep(3)

def search(start, end, cnt):
    ans = -1
    for i in range(cnt):
        #print(i, "==>", start, '~', end)
        mid = (start + end) // 2
        s = ''
        for n in range(start, mid):
            s += str(n) + ' '
        s += str(mid)
        sl(s)
        res = int(ru('\n')[:-1])
        #print(res)
        if res % 10 == 0:
            if start + 1 == end:
                ans = end
                break
            start = mid + 1
        elif res == 9:
            ans = start
            break
        else:
            end = mid
    while i < cnt - 1:
        i += 1
        sl(str(ans))
    return ans

for i in range(100):
    ru('N=')
    n = int(ru(' ')[:-1])
    ru('C=')
    c = int(ru('\n')[:-1])
    info('n = ' + str(n))
    info('c = ' + str(c))
    ans = search(0, n, c)
    info('ans = ' + str(ans))
    assert ans != -1
    sl(str(ans))
    print(ru('\n'))

p.interactive()

