from pwn import *
context.log_level = 'debug'
r = remote('47.94.129.246', 10003)
test = [0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1]
buf = [ch for ch in range(33, 127)]
buf2 = [ch for ch in range(33, 127)]
used = [0 for i in range(len(buf))]
res = []
for i in range(len(buf)):
    c = 0
    while True:
        if buf[i] == 0:
            break
        c ^= buf[i]
        buf[i] >>= 1
    res.append(c)
payload = ''
for i in range(len(test)):
    for j in range(len(res)):
        t = res[j] & 1
        if used[j] == 0 and t == test[i]:
            used[j] = 1
            payload += chr(buf2[j])
            break
r.sendline(payload)
r.interactive()