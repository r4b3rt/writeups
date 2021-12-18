#!/usr/bin/env python
key = 'qweee'
check = [0xFFFFFC49, 0x68, 0x10, 0xFFFFCC30, 0x3A71, 0x3878, 0xE7, 0xFFFFFF11]

def init_box(key):
    s_box = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s_box[i] + ord(key[i % len(key)])) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box

def crypto(s_box, data):
    res = []
    i = j = 0
    for d in data:
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        t = (s_box[i] + s_box[j]) % 256
        k = s_box[t]
        res.append(d ^ k)
    return res

def crack():
    for c0 in range(10):
        for c1 in range(10):
            for c2 in range(10):
                for c3 in range(10):
                    for c4 in range(10):
                        for c5 in range(10):
                            for c6 in range(10):
                                for c7 in range(10):
                                    try:
                                        data = [0x0000008A, 0x000001A1, 0x0000012A, 0x00000269, 0x00000209, 0x00000068, 0x0000039F, 0x000002C8]
                                        choices = str(c0) + str(c1) + str(c2) + str(c3) + str(c4) + str(c5) + str(c6) + str(c7)
                                        choices = '61495072'
                                        print choices
                                        for c in choices:
                                            if c == '0':
                                                data[2] = (data[2] & data[6]) & 0xFFFFFFFF
                                                data[3] = (data[3] * data[2]) & 0xFFFFFFFF
                                            elif c == '1':
                                                data[2] = (data[2] / data[3]) & 0xFFFFFFFF
                                                data[1] = (data[1] + data[5]) & 0xFFFFFFFF
                                            elif c == '2':
                                                data[4] = (data[4] ^ data[5]) & 0xFFFFFFFF
                                                data[7] = (data[7] + data[0]) & 0xFFFFFFFF
                                            elif c == '3':
                                                data[7] = (data[7] - data[4]) & 0xFFFFFFFF
                                                data[4] = (data[4] & data[1]) & 0xFFFFFFFF
                                            elif c == '4':
                                                data[5] = (data[5] * data[0]) & 0xFFFFFFFF
                                                data[3] = (data[3] - data[6]) & 0xFFFFFFFF
                                            elif c == '5':
                                                data[0] = (data[0] ^ data[3]) & 0xFFFFFFFF
                                                data[6] = (data[6] - data[7]) & 0xFFFFFFFF
                                            elif c == '6':
                                                data[5] = (data[5] | (data[1] / data[7])) & 0xFFFFFFFF
                                                data[1] = (data[1] / data[7]) & 0xFFFFFFFF
                                            elif c == '7':
                                                data[6] = (data[6] + data[2]) & 0xFFFFFFFF
                                                data[5] = (data[5] | data[1]) & 0xFFFFFFFF
                                            elif c == '8':
                                                data[0] = (data[0] * data[3]) & 0xFFFFFFFF
                                                data[4] = (data[4] - data[7]) & 0xFFFFFFFF
                                            elif c == '9':
                                                data[2] = (data[2] + data[5]) & 0xFFFFFFFF
                                                data[3] = (data[3] ^ data[4]) & 0xFFFFFFFF
                                            else:
                                                print '[!] Error'
                                                exit()
                                        if data == check:
                                            print '[*] Cracked =>', choices
                                            return choices
                                    except Exception:
                                        continue
s_box = init_box(key)
ciphertext = crack()
ciphertext = [int(c) for c in ciphertext]
plaintext = crypto(s_box, ciphertext)
plaintext = ''.join([hex(c)[2:].zfill(2) for c in plaintext])
print plaintext

