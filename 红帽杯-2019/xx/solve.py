#!/usr/bin/env python

def shift(z, y, x, k, p, e):
    return ((((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((x ^ y) + (k[(p & 3) ^ e] ^ z)))

def decrypt(v, k):
    delta = 0x9E3779B9
    n = len(v)
    rounds = 6 + 52 / n
    x = (rounds * delta) & 0xFFFFFFFF
    y = v[0]
    for i in range(rounds):
        e = (x >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] -= shift(z, y, x, k, p, e)
            v[p] = v[p] & 0xFFFFFFFF
            y = v[p]
        p -= 1
        z = v[n - 1]
        v[0] -= shift(z, y, x, k, p, e)
        v[0] = v[0] & 0xFFFFFFFF
        y = v[0]
        x -= delta
        x = x & 0xFFFFFFFF
    return v

ori_enc = [0xCE, 0xBC, 0x40, 0x6B, 0x7C, 0x3A, 0x95, 0xC0, 0xEF, 0x9B, 0x20, 0x20, 0x91, 0xF7, 0x02, 0x35, 0x23, 0x18, 0x02, 0xC8, 0xE7, 0x56, 0x56, 0xFA]
mixed_enc = []
for i in range(7, -1, -1):
    res = []
    for j in range(3):
        tmp = ori_enc[3*i+j]
        for k in range(i):
            tmp ^= ori_enc[k]
        res.append(tmp)
    mixed_enc = res + mixed_enc
enc = []
for i in range(len(mixed_enc) / 4):
    enc.append(mixed_enc[4*i+1])
    enc.append(mixed_enc[4*i+3])
    enc.append(mixed_enc[4*i])
    enc.append(mixed_enc[4*i+2])
dword_enc = []
for i in range(len(enc) / 4):
    dword_enc.append(enc[4*i] | enc[4*i+1]<<8 | enc[4*i+2]<<16 | enc[4*i+3]<<24)
key = map(ord, 'flag'.ljust(16, '\x00'))
dword_key = []
for i in range(len(key) / 4):
    dword_key.append(key[4*i] | key[4*i+1]<<8 | key[4*i+2]<<16 | key[4*i+3]<<24)
plaintext = decrypt(dword_enc, dword_key)
flag = ''
for i in range(len(plaintext)):
    flag += chr(plaintext[i] & 0xFF)
    flag += chr((plaintext[i] >> 8) & 0xFF)
    flag += chr((plaintext[i] >> 16) & 0xFF)
    flag += chr((plaintext[i] >> 24))
print flag

