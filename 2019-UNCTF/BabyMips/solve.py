#!/usr/bin/env python
import string

base64_charset = '/EXHYI6sc9RJPZyeqWi2QbNdh5uDL1MonwfS8VKxUrvF03lAGt7OgBk+zjC4Tmpa='

def rc4(text, key):
    result = ''
    key_len = len(key)
    #1. init S-box
    box = list(range(256))#put 0-255 into S-box
    j = 0
    for i in range(256):#shuffle elements in S-box according to key
        j = (j + box[i] + ord(key[i%key_len]))%256
        box[i],box[j] = box[j],box[i]#swap elements
    #2. make sure all elements in S-box swapped at least once
    i = j = 0
    for element in text:
        i = (i+1)%256
        j = (j+box[i])%256
        box[i],box[j] = box[j],box[i]
        k = chr(ord(element) ^ box[(box[i]+box[j])%256])
        result += k
    return result

def valid_base64_str(b_str):
    if len(b_str) % 4:
        print '[!] not base64 string...'
        return False

    for m in b_str:
        if m not in base64_charset:
            print '[!] charset %c invalid...' % (m)
            return False
    return True

def decipher(base64_str):
    if not valid_base64_str(base64_str):
        return bytearray()

    base64_bytes = ['{:0>6}'.format(str(bin(base64_charset.index(s))).replace('0b', '')) for s in base64_str if
                    s != '=']
    resp = bytearray()
    nums = len(base64_bytes) // 4
    remain = len(base64_bytes) % 4
    integral_part = base64_bytes[0:4 * nums]

    while integral_part:
        tmp_unit = ''.join(integral_part[0:4])
        tmp_unit = [int(tmp_unit[x: x + 8], 2) for x in [0, 8, 16]]
        for i in tmp_unit:
            resp.append(i)
        integral_part = integral_part[4:]

    if remain:
        remain_part = ''.join(base64_bytes[nums * 4:])
        tmp_unit = [int(remain_part[i * 8:(i + 1) * 8], 2) for i in range(remain - 1)]
        for i in tmp_unit:
            resp.append(i)

    return resp

enc = [0x00000042, 0xffffffe3, 0xffffffe3, 0x00000058, 0xffffffb9, 0xffffffec, 0xffffffbb, 0x00000016, 0x00000006, 0x00000024, 0xffffff93, 0xffffffa6, 0x00000068, 0x00000024, 0xffffffec, 0x0000007b, 0xffffffdc, 0x00000056, 0x00000015, 0xffffffeb, 0x0000006e, 0xffffffc8, 0x0000003c, 0xfffffff3, 0xffffff9c, 0x00000046, 0xffffffc4, 0x00000027, 0x0000001c, 0xffffffd1, 0xffffff99, 0xffffff80, 0x00000051, 0x00000005, 0x00000049, 0xffffffcb, 0x0000005c, 0xffffffb6, 0xffffff82, 0xffffffb2, 0xffffffd0, 0x00000072, 0x00000004, 0xffffffb6]
key = [0x5a, 0x4f, 0x36, 0x4b, 0x71, 0x37, 0x39, 0x4c, 0x26, 0x43, 0x50, 0x57, 0x76, 0x4e, 0x6f, 0x70, 0x7a, 0x51, 0x66, 0x67, 0x68, 0x44, 0x52, 0x53, 0x47, 0x40, 0x64, 0x69, 0x2a, 0x6b, 0x41, 0x42, 0x38, 0x72, 0x73, 0x46, 0x65, 0x77, 0x78, 0x6c, 0x6d, 0x2b, 0x2f, 0x75, 0x35, 0x61, 0x5e, 0x32, 0x59, 0x74, 0x54, 0x4a, 0x55, 0x56, 0x45, 0x6e, 0x30, 0x24, 0x48, 0x49, 0x33, 0x34, 0x79, 0x23]
key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
enc = ''.join(chr(c & 0xFF) for c in enc)
print enc
enc2 = rc4(enc, key)
print enc2
plaintext = decipher(enc2)
print plaintext

