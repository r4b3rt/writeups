#!/usr/bin/env python
import hashlib

def SHF(data):
    v4 = 0x2FD2B4
    for i in range(len(data)):
        low = data[i] ^ (v4 & 0xFFFFFFFF)
        v4 = (v4 & 0xFFFFFFFF00000000) | (low)
        v4 *= 0x66EC73
        v4 &= 0xFFFFFFFFFFFFFFFF
    return v4

def flag(e):
    target = 0x67616C46
    v4 = ((e & 0xFF) - 0x7D) & 0xFF
    v5 = (((e >> 8) & 0xFF) + 0x7C) & 0xFF
    v6 = (((e >> 16) & 0xFFFF) - 0x5100) & 0xFFFF
    res = v6 << 16 | v5 << 8 | v4
    #print hex(res)
    if res == target:
        return True
    else:
        return False

with open('output.png', 'rb') as f:
    ciphertext = f.read()

raw = []
for c in ciphertext:
    raw.append(ord(c))

def swap(raw):
    res = []
    tmp = []
    for i in range(15):
        tmp.append(raw[i * 0x1000:(i + 1) * 0x1000])
    for i in range(7):
        if (tmp[2 * i][0] + tmp[2 * i + 1][0]) & 1 == 0:
            tmp[2 * i], tmp[2 * i + 1] = tmp[2 * i + 1], tmp[2 * i]
    for arr in tmp:
        for c in arr:
            res.append(c)
    return res

raw[0x00 * 0x1000 + 0x0A] = 7
raw[0x0D * 0x1000 + 0x0A] = 12

def check(raw, arr):
    a, b, c, d, e, f, g, h, i, j, k, l = arr
    raw[0x01 * 0x1000 + 0x0A] = a
    raw[0x02 * 0x1000 + 0x0A] = b
    raw[0x03 * 0x1000 + 0x0A] = c
    raw[0x04 * 0x1000 + 0x0A] = d
    raw[0x05 * 0x1000 + 0x0A] = e
    raw[0x06 * 0x1000 + 0x0A] = f

    raw[0x07 * 0x1000 + 0x0A] = g
    raw[0x09 * 0x1000 + 0x0A] = i
    raw[0x0A * 0x1000 + 0x0A] = j
    raw[0x0B * 0x1000 + 0x0A] = k
    raw[0x0C * 0x1000 + 0x0A] = l

    raw[0x08 * 0x1000 + 0x0A] = h

    res = SHF(raw) # 0x0040FE73B861F0C3
    if flag(res) == True:
        raw = swap(raw)
        with open('data', 'wb') as f:
            for c in raw:
                f.write(chr(c))
        print 'Success'
        return True

def bruteforce(raw):
    for a in range(0x34, 0x3E):
        for b in range(0x34, 0x3E):
            for c in range(0x34, 0x3E):
                if (a ** 3 + b ** 3 + c ** 3) & 0xFF != 0x62:
                    continue
                #print 'Break 1'
                for d in range(0x34, 0x3E):
                    for e in range(0x34, 0x3E):
                        for f in range(0x34, 0x3E):
                            for g in range(0x4D, 0x57):
                                if (d ** 3 + e ** 3 + f ** 3 + g ** 3) & 0xFF != 0x6B:
                                    continue
                                #print 'Break 2'
                                for i in range(0x4D, 0x57):
                                    for j in range(0x4D, 0x57):
                                        for k in range(0x4D, 0x57):
                                            for l in range(0x22, 0x2C):
                                                if (i ** 3 + j ** 3 + k ** 3 + l ** 3) & 0xFF != 0xBF:
                                                    continue
                                                #print 'Break 3'
                                                for h in range(0x4D, 0x57):
                                                    arr = [a, b, c, d, e, f, g, h, i, j, k, l]
                                                    #arr = [0x36, 0x3D, 0x3D, 0x3B, 0x38, 0x3A, 0x50, 0x53, 0x4F, 0x55, 0x53, 0x26]
                                                    if check(raw, arr):
                                                        return True

bruteforce(raw)

def get_flag():
    with open('data', 'rb') as f:
        data = f.read()
    data = [ord(c) for c in data]
    flag = SHF(data)
    return 'WhiteHat{' + hashlib.sha1(str(flag)).hexdigest() + '}'

print get_flag()

